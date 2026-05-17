import os
import sys
import glob
import shutil
import uuid
import asyncio
import subprocess

from importlib.util import find_spec

DEFAULT_LIBRARY = ""
DEFAULT_API_ID = ""
DEFAULT_API_HASH = ""
DEFAULT_PHONE_NUMBER = ""

MAX_RETRY = 3


def run(cmd):

    return subprocess.run(
        cmd,
        shell=True,
        capture_output=True,
        text=True
    )


def install(pkg):

    module = pkg.replace("-", "_")

    if find_spec(module) is None:

        print(f"\nInstalling {pkg}...\n")

        x = run(
            f"pip install -q {pkg}"
        )

        if x.returncode != 0:

            print(x.stderr)

            sys.exit(1)


def ask(text, default=""):

    for _ in range(MAX_RETRY):

        value = (
            input(
                f"{text}"
                f"{f' [{default}]' if default else ''}: "
            )
            .strip()
            or default
        )

        if value:
            return value

        print("Invalid Value")

    sys.exit(1)


print(
    "\nTelegram Session Generator\n"
)

print(
    "Supported Libraries:\n"
    "- pyrogram\n"
    "- pyrofork\n"
    "- any pyrogram fork\n"
)

MODE = ask(
    "Choose Login Method (1 = Phone Number, 2 = Session String)",
    "1"
)

LIBRARY = ask(
    "Library Name",
    DEFAULT_LIBRARY
).lower()

API_ID = ask(
    "API ID",
    DEFAULT_API_ID
)

API_HASH = ask(
    "API HASH",
    DEFAULT_API_HASH
)

PHONE_NUMBER = ""
OLD_SESSION = ""


if MODE == "1":

    API_ID = ask(
        "API ID",
        DEFAULT_API_ID
    )

    API_HASH = ask(
        "API HASH",
        DEFAULT_API_HASH
    )

    PHONE_NUMBER = ask(
        "Phone Number",
        DEFAULT_PHONE_NUMBER
    )

elif MODE == "2":

    API_ID = ask(
        "API ID",
        DEFAULT_API_ID
    )

    API_HASH = ask(
        "API HASH",
        DEFAULT_API_HASH
    )

    OLD_SESSION = ask(
        "Old Session String"
    )
    

else:

    print("Invalid Mode")

    sys.exit(1)

install(LIBRARY)
install("tgcrypto")

try:

    from pyrogram import Client

    from pyrogram.errors import (
        SessionPasswordNeeded,
        PhoneCodeInvalid,
        PasswordHashInvalid
    )

except Exception as e:

    print(e)

    sys.exit(1)

for i in (
    glob.glob("USER*")
    + glob.glob("*.session*")
):

    try:

        shutil.rmtree(i) if os.path.isdir(i) else os.remove(i)

    except:
        pass

SESSION = (
    f"USER_{uuid.uuid4().hex}"
)

if MODE == "1":

    app = Client(
        SESSION,
        api_id=int(API_ID),
        api_hash=API_HASH,
        phone_number=PHONE_NUMBER,
        in_memory=False 
    )

else:

    app = Client(
        SESSION,
        api_id=int(API_ID),
        api_hash=API_HASH,
        session_string=OLD_SESSION,
        in_memory=False
    )


async def main():

    try:

        await app.connect()

        if MODE == "1":

            sent = None

            for _ in range(MAX_RETRY):

                try:

                    sent = await app.send_code(
                        PHONE_NUMBER
                    )

                    break

                except Exception as e:

                    print(e)

            if not sent:

                raise Exception(
                    "Failed Sending OTP"
                )

            ok = False

            for _ in range(MAX_RETRY):

                try:

                    otp = input(
                        "\nEnter OTP: "
                    ).strip()

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

                    print(
                        "Invalid OTP"
                    )

                except Exception as e:

                    print(e)

            if not ok:

                for _ in range(MAX_RETRY):

                    try:

                        pw = input(
                            "\nEnter 2FA Password: "
                        ).strip()

                        await app.check_password(
                            password=pw
                        )

                        ok = True

                        break

                    except PasswordHashInvalid:

                        print(
                            "Wrong Password"
                        )

                    except Exception as e:

                        print(e)

            if not ok:

                raise Exception(
                    "Login Failed"
                )

        me = await app.get_me()

        session = await app.export_session_string()

        try:

            text = (
                f"**Tʜɪs Is Yᴏᴜʀ "
                f"__{LIBRARY}__ "
                f"Sᴛʀɪɴɢ Sᴇssɪᴏɴ**\n\n"
                f"`{session}`\n\n"
                f"⚠️ **Dᴏɴ'ᴛ Sʜᴀʀᴇ "
                f"Tʜɪs Wɪᴛʜ Aɴʏᴏɴᴇ**"
            )

            await app.send_message(
                "me",
                text
            )

        except Exception as e:

            print(e)

        print(
            f"\nSession Generated Successfully "
            f"for @{me.username or me.first_name}"
        )

    except Exception as e:

        print(f"\n{e}")

    finally:
    
        try:
    
            app.storage.SESSION_STRING = None
    
            await app.disconnect()
    
        except:
            pass
    
        for i in (
            glob.glob("USER*")
            + glob.glob("*.session*")
        ):
    
            try:
    
                shutil.rmtree(i) if os.path.isdir(i) else os.remove(i)
    
            except:
                pass
    
        try:
    
            print(
                f"\nUninstalling {LIBRARY} and tgcrypto...\n"
            )
    
            run(
                f"pip uninstall -y {LIBRARY} tgcrypto"
            )
    
        except Exception as e:
    
            print(e)
    
        print(
            "\nSession Files Cleaned"
        )


asyncio.run(main())