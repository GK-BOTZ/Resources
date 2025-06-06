# 🚀 Advanced Termux Usage Guide

> Unlock the real power of Termux with pro-level features, tools, and configs.

---

## ⚙️ Recommended Advanced Packages

```bash
pkg install -y tmux neofetch htop proot-distro openssh nmap python-dev clang cmake
```

| Tool            | Purpose                                      |
|-----------------|----------------------------------------------|
| `tmux`          | Persistent sessions, multitasking in terminal |
| `neofetch`      | System info display                          |
| `htop`          | Interactive process viewer                   |
| `proot-distro`  | Run full Linux distros inside Termux         |
| `openssh`       | SSH into Termux from other devices           |
| `nmap`          | Network scanning & diagnostics               |

---

## 🧱 Use Linux Distros Inside Termux

```bash
pkg install proot-distro
proot-distro list
proot-distro install debian
proot-distro login debian
```

You now have a full Debian environment inside Termux — run `apt`, `systemctl`, even install full desktop environments.

---

## 🖥️ Setup SSH Server in Termux

```bash
pkg install openssh
sshd
ifconfig  # Note your IP
```

Connect from another machine:

```bash
ssh username@<your-ip> -p 8022
```

Default username is `u0_aXXX` and password is disabled (use SSH key or termux API).

---

## 📦 Compile Native Python Packages

To compile packages like `cryptography`, `lxml`, etc:

```bash
pkg install clang python-dev libffi-dev openssl-dev
```

Now install with pip:

```bash
pip install cryptography
```

---

## 💻 Terminal Multiplexing with `tmux`

```bash
tmux
```

- `Ctrl+b c` → New window  
- `Ctrl+b n` → Next window  
- `Ctrl+b d` → Detach  
- `tmux attach` → Reattach session

Useful for background jobs or multitasking in a single Termux session.

---

## 🌍 Networking Tools

```bash
pkg install nmap net-tools curl dnsutils
```

Scan network or inspect connections:
```bash
nmap -sP 192.168.1.0/24
netstat -tuln
```

---

## 🧠 Developer Workflow Tips

- Always use `venv` for Python projects.
- Use `pip freeze > requirements.txt` for exporting environments.
- Use `tmux` when working on long-running scripts.
- Set up `alias` in `~/.bashrc` or `~/.zshrc`:

```bash
alias py='python'
alias gs='git status'
alias ga='git add .'
```

---

## 🔐 Secure Termux

- Do not share your `.termux` directory or SSH keys.
- Be careful with `storage` access via `termux-setup-storage`.
- Use `iptables` if needed for network restrictions.

---

## 📦 Useful Pip Packages

```bash
pip install ipython httpie rich pyfiglet flask requests
```

| Package     | Use Case                     |
|-------------|------------------------------|
| `ipython`   | Enhanced Python REPL         |
| `httpie`    | CLI HTTP client (better curl)|
| `rich`      | Beautiful terminal output    |
| `flask`     | Micro web framework          |
| `requests`  | HTTP requests for Python     |

---

## 🧬 Bonus: Run GUI Apps via VNC (Pro)

Install proot-distro, set up Ubuntu/Xfce:

```bash
proot-distro install ubuntu
proot-distro login ubuntu
apt update && apt install xfce4 xfce4-goodies tightvncserver
```

Then set up `vncserver` and connect via VNC Viewer app.

---

## ✅ Summary

You're now beyond the basics. Termux can act as:

- A full dev environment
- A penetration testing toolkit
- A portable Linux distro
- A Python powerhouse

> Your Android is now your Linux workstation.

