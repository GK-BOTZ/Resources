import os, sys, glob, shutil, uuid, asyncio, subprocess
from importlib.util import find_spec

DEFAULT_LIBRARY = ""
DEFAULT_API_ID = ""
DEFAULT_API_HASH = ""
DEFAULT_PHONE_NUMBER = ""

MAX_RETRY = 3

def run(cmd):
    return subprocess.run(cmd, shell=True, capture_output=True, text=True)

def install(pkg):
    module = pkg.replace("-", "_")
    if find_spec(module) is None:
        print(f"\nInstalling {pkg}...\n")
        x = run(f"pip install -q {pkg}")
        if x.returncode != 0:
            print(x.stderr)
            sys.exit(1)

def ask(text, default=""):
    for _ in range(MAX_RETRY):
        x = input(f"{text}{f' [{default}]' if default else ''}: ").strip() or default
        if x:
            return x
        print("Invalid Value")
    sys.exit(1)

print("\nTelegram Session Generator\n")
print("Supported Libraries:\n- pyrogram\n- pyrofork\n- any pyrogram fork\n")

LIBRARY = ask("Library Name", DEFAULT_LIBRARY).lower()
API_ID = ask("API ID", DEFAULT_API_ID)
API_HASH = ask("API HASH", DEFAULT_API_HASH)
PHONE_NUMBER = ask("Phone Number", DEFAULT_PHONE_NUMBER)

install(LIBRARY)
install("tgcrypto")

try:
    from pyrogram import Client
    from pyrogram.errors import SessionPasswordNeeded, PhoneCodeInvalid, PasswordHashInvalid
except Exception as e:
    print(e)
    sys.exit(1)

for i in glob.glob("USER*") + glob.glob("*.session*"):
    try:
        shutil.rmtree(i) if os.path.isdir(i) else os.remove(i)
    except:
        pass

SESSION = f"USER_{uuid.uuid4().hex}"

app = Client(
    SESSION,
    api_id=int(API_ID),
    api_hash=API_HASH,
    phone_number=PHONE_NUMBER,
    in_memory=True
)

async def main():
    try:
        await app.connect()

        sent = None

        for _ in range(MAX_RETRY):
            try:
                sent = await app.send_code(PHONE_NUMBER)
                break
            except Exception as e:
                print(e)

        if not sent:
            raise Exception("Failed Sending OTP")

        ok = False

        for _ in range(MAX_RETRY):
            try:
                otp = input("\nEnter OTP: ").strip()

                await app.sign_in(
                    PHONE_NUMBER,
                    sent.phone_code_hash,
                    otp
                )

                ok = True
                break

            except SessionPasswordNeeded:
                break

            except PhoneCodeInvalid:
                print("Invalid OTP")

            except Exception as e:
                print(e)

        if not ok:

            for _ in range(MAX_RETRY):

                try:
                    pw = input("\nEnter 2FA Password: ").strip()

                    await app.check_password(password=pw)

                    ok = True
                    break

                except PasswordHashInvalid:
                    print("Wrong Password")

                except Exception as e:
                    print(e)

        if not ok:
            raise Exception("Login Failed")

        session = await app.export_session_string()
        me = await app.get_me()

        try:
            text = f"**Tʜɪs Is Yᴏᴜʀ __{LIBRARY}__ Sᴛʀɪɴɢ Sᴇssɪᴏɴ**\n\n`{session}`\n\n⚠️ **Dᴏɴ'ᴛ Sʜᴀʀᴇ Tʜɪs Wɪᴛʜ Aɴʏᴏɴᴇ**"
            await app.send_message("me", text)
        except Exception as e:
            print(e)

        print(f"\nSession Generated Successfully for @{me.username or me.first_name}")

    except Exception as e:
        print(f"\n{e}")

    finally:

        try:
            app.storage.SESSION_STRING = None
            await app.disconnect()
        except:
            pass

        for i in glob.glob("USER*") + glob.glob("*.session*"):
            try:
                shutil.rmtree(i) if os.path.isdir(i) else os.remove(i)
            except:
                pass

        try:
            print(f"\nUninstalling {LIBRARY} and tgcrypto...\n")
            run(f"pip uninstall -y {LIBRARY} tgcrypto")
        except Exception as e:
            print(e)

        print("\nSession Files Cleaned")

asyncio.run(main())
