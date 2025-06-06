# 📱 Termux Python Dev Setup Guide

> Fast, minimal, no bloat — just what you need as a Python dev.

[Download Termux from Google Play Store →](https://play.google.com/store/apps/details?id=com.termux)

---

## 🚀 Why Termux?

Termux gives you a powerful Linux environment right on your Android device. Ideal for coding, scripting, or running Python apps — without root, without hacks.

---

## 🔧 Step-by-Step Setup

### 1. Update System
```bash
pkg update -y && pkg upgrade -y
```

Keeps everything up-to-date and avoids broken packages.

---

### 2. Install Core Packages
```bash
pkg install -y python git clang build-essential libffi openssl
```

| Package         | Purpose                                      |
|-----------------|----------------------------------------------|
| `python`        | The main language you'll work with           |
| `git`           | Version control and cloning repos            |
| `clang`         | C compiler (used in pip builds)              |
| `build-essential` | Compilation tools (make, g++, etc.)       |
| `libffi`, `openssl` | Needed for some Python packages         |

---

### 3. Upgrade Python Toolchain
```bash
python -m ensurepip
pip install --upgrade pip setuptools wheel
```

Keeps pip and its helpers in sync and ready to install any package.

---

### 4. Optional Utilities (Recommended)
```bash
pkg install -y vim nano curl wget unzip zip tar
```

Good to have editors and tools around.

---

### 5. Create and Use Virtual Environments
```bash
python -m venv myenv
source myenv/bin/activate
```

✅ Keeps your project dependencies clean and isolated.

---

### 6. Fix Common pip/SSL Issues (if needed)
```bash
pip config set global.cert /data/data/com.termux/files/usr/etc/tls/cert.pem
```

Helps when pip complains about SSL or certificates.

---

## ✅ You’re Ready.

Use Git to clone repos, `pip` to install packages, `venv` to isolate projects — all from your phone.

No fluff. Just power.

---

### Pro 😎 (All In One) ####
```
pkg update -y && pkg upgrade -y && pkg install -y python git clang build-essential libffi openssl vim curl wget unzip tar && python -m ensurepip && pip install -U pip setuptools wheel
```
### 📎 Bonus Tips

- Use `tmux` to keep sessions alive.
- Run `alias py='python'` for convenience.
- Install `httpie`, `rich`, `ipython`, or any other dev tool via pip.

---

**Happy coding from Termux!**  
Built for hackers, coders, and devs — like you.

