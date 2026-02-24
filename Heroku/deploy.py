#!/usr/bin/env python3
import os
import sys
import json
import subprocess
import argparse
from pathlib import Path
import threading
import sys
import termios
import tty

    
# ===== DEFAULTS =====
DEFAULT_APP = "my-default-app"
DEFAULT_TEAM = None
DEFAULT_REPO = None
DEFAULT_BRANCH = "master"
DEFAULT_ENV_FILE = "config.env"
DEFAULT_EMAIL = ""
DEFAULT_API_KEY = ""
SETTINGS_FILE = ".hk.json"
AUTH_FILE = Path.home() / ".hk_auth.json"

parser = argparse.ArgumentParser()

parser.add_argument("-a", "--app")
parser.add_argument("-t", "--team")
parser.add_argument("-url", "--repo")
parser.add_argument("-b", "--branch")
parser.add_argument("-e", "--env", action="append")
parser.add_argument("-file", "--file")
parser.add_argument("-mail", "--email")
parser.add_argument("-api", "--api_key")
parser.add_argument("-c", "--container", action="store_true")
parser.add_argument("-d", "--deploy", action="store_true")
parser.add_argument("-l", "--logs", action="store_true", help="Show logs")
parser.add_argument("-f", "--follow", action="store_true", help="Follow logs live")
parser.add_argument("-n", "--lines", type=int, default=100, help="Number of log lines")
parser.add_argument("command", nargs="?", help="login | logout")

args = parser.parse_args()

APP = args.app if args.app else DEFAULT_APP
TEAM = args.team if args.team else DEFAULT_TEAM
REPO = args.repo if args.repo else DEFAULT_REPO
BRANCH = args.branch if args.branch else DEFAULT_BRANCH
ENV_VARS = args.env or []
ENV_FILE = args.file if args.file else DEFAULT_ENV_FILE
EMAIL = args.email if args.email else DEFAULT_EMAIL
API_KEY = args.api_key if args.api_key else DEFAULT_API_KEY
IS_CONTAINER = args.container or False
DEPLOY_ONLY = args.deploy


def setup_auth():
    auth = load_auth()

    if not auth:
        print("Not logged in. Run: hk login")
        sys.exit(1)

    os.environ["HEROKU_API_KEY"] = auth["api_key"]
    
def login_auth():
    email = input("Heroku Email: ").strip()
    api_key = input("Heroku API Key: ").strip()

    if not email or not api_key:
        print("Both email and API key required.")
        sys.exit(1)

    save_auth(email, api_key)

def logout_auth():
    if AUTH_FILE.exists():
        AUTH_FILE.unlink()
        print("Logged out successfully.")
    else:
        print("Already logged out.")

def load_auth():
    if AUTH_FILE.exists():
        with open(AUTH_FILE) as f:
            return json.load(f)
    return None
    
def save_auth(email, api_key):
    data = {"email": email, "api_key": api_key}
    with open(AUTH_FILE, "w") as f:
        json.dump(data, f)
    os.chmod(AUTH_FILE, 0o600)
    print("Login saved.")

def ensure_git_identity():
    email = subprocess.run(
        "git config user.email",
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=True
    ).stdout.strip()

    if not email:
        run('git config --global user.email "deploy@local"')
        run('git config --global user.name "deploy-bot"')
        
def _wait_for_keypress(stop_event):
    try:
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        tty.setcbreak(fd)
        sys.stdin.read(1)
        stop_event.set()
    except:
        pass
    finally:
        try:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        except:
            pass

def stream_logs():
    print("\nStreaming logs (Press CTRL+C or any key to stop)\n")

    stop_event = threading.Event()

    key_thread = threading.Thread(
        target=_wait_for_keypress,
        args=(stop_event,),
        daemon=True
    )
    key_thread.start()

    process = subprocess.Popen(
        f"heroku logs -a {APP} --tail",
        shell=True
    )

    try:
        while process.poll() is None:
            if stop_event.is_set():
                process.terminate()
                break
    except KeyboardInterrupt:
        process.terminate()

    print("\nLog streaming stopped.\n")


def show_logs():
    cmd = f"heroku logs -a {APP} --num {args.lines}"

    if args.follow:
        cmd += " --tail"

    run(cmd)
    
def load_settings():
    if Path(SETTINGS_FILE).exists():
        with open(SETTINGS_FILE) as f:
            return json.load(f)
    return None

if args.deploy:
    cfg = load_settings()
    if cfg:
        APP = cfg["app"]
        BRANCH = cfg["branch"]
        
if args.logs:
    cfg = load_settings()
    if cfg:
        APP = cfg["app"]
        
def save_settings():
    data = {
        "app": APP,
        "branch": BRANCH,
    }
    with open(SETTINGS_FILE, "w") as f:
        json.dump(data, f)


def delete_settings():
    if Path(SETTINGS_FILE).exists():
        Path(SETTINGS_FILE).unlink()
        
def get_app_dir():
    cwd = Path.cwd()
    if cwd.name == APP:
        return cwd
    return cwd / APP
    
def run(cmd):
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        sys.exit(result.returncode)

def write_env():
    if not ENV_VARS:
        return

    app_dir = get_app_dir()
    app_dir.mkdir(exist_ok=True)

    env_path = app_dir / ENV_FILE
    existing = {}

    if env_path.exists():
        with open(env_path) as f:
            for line in f:
                if "=" in line:
                    k, v = line.strip().split("=", 1)
                    existing[k] = v

    for item in ENV_VARS:
        if "=" not in item:
            continue
        k, v = item.split("=", 1)
        existing[k.strip()] = v.strip()

    with open(env_path, "w") as f:
        for k, v in existing.items():
            f.write(f"{k}={v}\n")

    print(f"Updated {env_path}")


def is_termux():
    return "com.termux" in os.environ.get("PREFIX", "")

def command_exists(cmd):
    return subprocess.run(
        f"command -v {cmd}",
        shell=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    ).returncode == 0

def install_heroku():
    if command_exists("heroku"):
        return

    print("Heroku CLI not found. Installing...")

    if is_termux():
        print("Detected Termux environment")

        if not command_exists("npm"):
            run("pkg install nodejs -y")

        run("npm install -g heroku")

    else:
        print("Detected Linux environment")

        # try official installer first
        if command_exists("curl"):
            run("curl https://cli-assets.heroku.com/install.sh | sh")
        else:
            run("apt update && apt install curl -y")
            run("curl https://cli-assets.heroku.com/install.sh | sh")

    print("Heroku CLI installed successfully.")
    

def app_exists():
    result = subprocess.run(
        f"heroku apps:info -a {APP}",
        shell=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    return result.returncode == 0


def create_app():
    run("rm -rf .venv venv env __pycache__")

    if app_exists():
        return

    if TEAM:
        if IS_CONTAINER:
            run(f"heroku apps:create {APP} --team {TEAM} --stack container")
        else:
            run(f"heroku apps:create {APP} --team {TEAM}")
    else:
        if IS_CONTAINER:
            run(f"heroku create {APP} --stack container")
        else:
            run(f"heroku create {APP}")
            
def clone_repo():
    if not REPO:
        return

    cwd = Path.cwd()

    if cwd.name == APP:
        print("Already inside repo. Skipping clone.")
        return

    if Path(APP).exists():
        print("Repo exists. skipping clone.")
        return

    run(f"git clone -b {BRANCH} {REPO} {APP}")    

def set_config_vars():
    for var in ENV_VARS:
        run(f"heroku config:set {var} -a {APP}")

def print_app_url():
    result = subprocess.check_output(
        f"heroku apps:info -a {APP}",
        shell=True,
        text=True
    )

    for line in result.splitlines():
        if "Web URL" in line:
            url = line.split(":", 1)[-1].strip()
            print(f"\n🌐 App URL: {url}\n")
            return
        
        
def deploy():
    cwd = Path.cwd().resolve()

    if cwd.name != APP:
        os.chdir(APP)

    ensure_git_identity()

    # always ensure container stack if requested
    if IS_CONTAINER:
        run(f"heroku stack:set container -a {APP}")

    # ensure new commit exists (forces deploy)
    run(f"git add -f {DEFAULT_ENV_FILE}")
    CONFIG_FILE = 'config.py'
    if CONFIG_FILE != DEFAULT_ENV_FILE and Path(CONFIG_FILE).exists():
        run(f"git add -f {CONFIG_FILE}")
        
    run('echo "$(date)" > .deploy-timestamp')
    run("git add -A")

    subprocess.run(
        'git commit -m "deploy" 2>/dev/null',
        shell=True
    )

    remote_url = f"https://heroku:{API_KEY}@git.heroku.com/{APP}.git"

    run("git remote remove heroku 2>/dev/null || true")
    run(f"git remote add heroku {remote_url}")

    push = subprocess.run(
        f"git push heroku HEAD:master -f",
        shell=True
    )

    if push.returncode == 0:
        print("\n✔ Deploy pushed successfully\n")
        return True
    else:
        print("\n✖ Deploy failed\n")
        return False
        
# ================= EXECUTION =================

if args.command == "login":
    login_auth()
    sys.exit(0)

if args.command == "logout":
    logout_auth()
    sys.exit(0)
    
if args.logs:
    setup_auth()
    show_logs()
    sys.exit(0)
    
if not DEPLOY_ONLY:
    install_heroku()
    setup_auth()
    create_app()
    clone_repo()
    write_env()
    set_config_vars()
    save_settings()
    
    print("Settings saved. Run 'hk -d' to deploy.")
    print_app_url()

    
else:
    setup_auth()
    deploy()
    delete_settings()
    stream_logs()
    
    print("Deploy completed.")
    print_app_url()
