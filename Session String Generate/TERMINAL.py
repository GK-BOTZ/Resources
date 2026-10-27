import os
import re
import sys
import uuid
import shutil
import asyncio
import getpass
import tempfile
import importlib
import subprocess
from importlib import metadata

DEFAULT_LIBRARY = os.getenv("TG_LIBRARY", "")
DEFAULT_API_ID = os.getenv("TG_API_ID", "")
DEFAULT_API_HASH = os.getenv("TG_API_HASH", "")
DEFAULT_PHONE_NUMBER = os.getenv("TG_PHONE", "")

MAX_RETRY = 3

# "wzgram", "wzgram==2.2.11", "wzgram == 2.2.11", "wzgram>=2.2,<2.3", "wzgram 2.2.11"
NAME_RE = re.compile(r"^([A-Za-z0-9][A-Za-z0-9._-]*)\s*(.*)$")
SPEC_RE = re.compile(r"^(===|==|~=|!=|<=|>=|<|>)\s*[A-Za-z0-9.*+!_-]+$")
BARE_VER_RE = re.compile(r"^[0-9][A-Za-z0-9.*+!_-]*$")


def canon(name):
    return re.sub(r"[-_.]+", "-", name).lower()


def parse_library(raw):
    """Returns (dist_name or None, pip_spec)."""
    raw = raw.strip()
    if raw.lower().startswith(("git+", "http://", "https://")):
        return None, raw

    m = NAME_RE.match(raw)
    if not m:
        raise ValueError("Invalid library name")

    name, rest = m.group(1), m.group(2).strip()
    if not rest:
        return name, name

    if BARE_VER_RE.match(rest):
        rest = "==" + rest

    parts = [p.strip() for p in rest.split(",")]
    if not all(SPEC_RE.match(p) for p in parts):
        raise ValueError(f"Invalid version specifier: {rest}")

    return name, name + ",".join(p.replace(" ", "") for p in parts)


def ask(text, default="", secret=False):
    for _ in range(MAX_RETRY):
        prompt = f"{text}{f' [{default}]' if default else ''}: "
        x = (getpass.getpass(prompt) if secret else input(prompt)).strip() or default
        if x:
            return x
        print("Invalid Value")
    sys.exit(1)


def pip_install(target, *pkgs):
    return subprocess.run(
        [
            sys.executable, "-m", "pip", "install", "-q",
            "--disable-pip-version-check", "--no-warn-script-location",
            "--target", target, *pkgs,
        ],
        capture_output=True,
        text=True,
    )


def find_dist(name, target):
    want = canon(name)
    for d in metadata.distributions(path=[target]):
        if canon(d.metadata["Name"] or "") == want:
            return d
    return None


def module_name_for(dist):
    # Forks like wzgram / pyrofork / kurigram still import as "pyrogram"
    if dist is not None:
        top = (dist.read_text("top_level.txt") or "").split()
        if "pyrogram" in top:
            return "pyrogram"
        if top:
            return top[0]
    return "pyrogram"


def load_library(raw, target):
    try:
        name, spec = parse_library(raw)
    except ValueError as e:
        print(e)
        sys.exit(1)

    print(f"\nInstalling {spec} (isolated, your environment stays untouched)...\n")
    r = pip_install(target, spec)
    if r.returncode != 0:
        print(r.stderr)
        sys.exit(1)

    # tgcrypto is optional (speeds up crypto, needs a compiler on some platforms)
    r = pip_install(target, "tgcrypto")
    if r.returncode != 0:
        print("tgcrypto could not be installed, continuing without it (slower).")

    # Make the isolated copy win over anything in site-packages
    sys.path.insert(0, target)
    importlib.invalidate_caches()

    dist = find_dist(name, target) if name else None
    modname = module_name_for(dist)

    try:
        lib = importlib.import_module(modname)
        errors = importlib.import_module(f"{modname}.errors")
    except Exception as e:
        print(f"Failed to import {modname}: {e}")
        sys.exit(1)

    shown = f"{dist.metadata['Name']} {dist.version}" if dist else spec
    print(f"Using {shown}\n")
    return lib, errors, shown


async def main(lib, errors, shown, api_id, api_hash, phone, workdir):
    Client = lib.Client
    name = f"USER_{uuid.uuid4().hex}"

    try:
        app = Client(name, api_id=api_id, api_hash=api_hash, in_memory=True)
    except TypeError:
        # very old versions without in_memory
        app = Client(name, api_id=api_id, api_hash=api_hash, workdir=workdir)

    try:
        await app.connect()

        sent = None
        for _ in range(MAX_RETRY):
            try:
                sent = await app.send_code(phone)
                break
            except errors.FloodWait as e:
                raise Exception(f"FloodWait: try again in {e.value} seconds")
            except (errors.PhoneNumberInvalid, errors.ApiIdInvalid) as e:
                raise Exception(str(e))
            except Exception as e:
                print(e)
                await asyncio.sleep(2)

        if not sent:
            raise Exception("Failed Sending OTP")

        signed_in = False
        needs_password = False

        for _ in range(MAX_RETRY):
            otp = re.sub(r"[\s-]", "", input("\nEnter OTP: "))
            try:
                await app.sign_in(phone, sent.phone_code_hash, otp)
                signed_in = True
                break
            except errors.SessionPasswordNeeded:
                needs_password = True
                break
            except errors.PhoneCodeInvalid:
                print("Invalid OTP")
            except errors.PhoneCodeExpired:
                print("OTP expired, sending a new one...")
                sent = await app.send_code(phone)
            except Exception as e:
                print(e)

        if needs_password:
            for _ in range(MAX_RETRY):
                pw = getpass.getpass("\nEnter 2FA Password: ")
                try:
                    await app.check_password(pw)
                    signed_in = True
                    break
                except errors.PasswordHashInvalid:
                    print("Wrong Password")
                except Exception as e:
                    print(e)

        if not signed_in:
            raise Exception("Login Failed")

        session = await app.export_session_string()
        me = await app.get_me()

        text = (
            f"**Tʜɪs Is Yᴏᴜʀ __{shown}__ Sᴛʀɪɴɢ Sᴇssɪᴏɴ**\n\n"
            f"`{session}`\n\n"
            f"⚠️ **Dᴏɴ'ᴛ Sʜᴀʀᴇ Tʜɪs Wɪᴛʜ Aɴʏᴏɴᴇ**"
        )
        try:
            await app.send_message("me", text)
            print("\nSession string sent to your Saved Messages.")
        except Exception as e:
            # never lose the session if sending fails
            print(f"\nCould not send to Saved Messages ({e}). Your session string:\n\n{session}\n")

        print(f"Session Generated Successfully for @{me.username or me.first_name}")

    except Exception as e:
        print(f"\n{e}")

    finally:
        try:
            await app.disconnect()
        except Exception:
            pass


if __name__ == "__main__":
    print("\nTelegram Session Generator\n")
    print("Supported Libraries (name or name==version):")
    print("- pyrogram, pyrofork, kurigram, wzgram==2.2.11, any pyrogram fork")
    print("- git+https://... URLs also work\n")

    library = ask("Library", DEFAULT_LIBRARY)
    api_id = ask("API ID", DEFAULT_API_ID)
    if not api_id.isdigit():
        print("API ID must be a number")
        sys.exit(1)
    api_hash = ask("API HASH", DEFAULT_API_HASH)
    phone = re.sub(r"[^\d+]", "", ask("Phone Number (with country code)", DEFAULT_PHONE_NUMBER))

    tmp = tempfile.mkdtemp(prefix="tgsession_")
    try:
        lib, errors, shown = load_library(library, tmp)
        asyncio.run(main(lib, errors, shown, int(api_id), api_hash, phone, tmp))
    except KeyboardInterrupt:
        print("\nCancelled")
    finally:
        # Removes the isolated library install and any temp session files
        shutil.rmtree(tmp, ignore_errors=True)
        print("\nTemporary files cleaned")
