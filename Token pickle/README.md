Here you go — this is your final .md file content, exactly as requested, professional and streamlined:

### 🔽 README.md

## 🔐 Token Generator for Google OAuth (`token.pickle`)

This tool allows you to securely generate a `token.pickle` for accessing Google APIs (Drive, Gmail, YouTube, etc.) using `credentials.json`.

---

## 🚀 Setup Instructions

### 1. Install Termux (If Not Already)

Download from the official repo:  
➡️ [Termux Releases](https://play.google.com/store/apps/details?id=com.termux)

Then open Termux and run:

--- 

``` bash
pkg update && pkg upgrade -y
pkg install git python python-pip -y
pip install --upgrade pip
```

---


### 2. Fork This Repository

https://github.com/GK-BOTZ/Token-Pickle/fork

---

### 3. Upload Your Credentials File
Now Upload Your `json` File And name it `credentials.json`

--- 

### 5. Clone The Repo
```bash
git clone https://github.com/YOUR_USERNAME/Token-Pickle
```

### 4. Install Python Requirements

```bash
pip install -r requirements.txt
```

---

### 5. Generate the Token

```bash
python3 generate.py
```

- Copy the URL shown in Termux.

- Open it in a browser.

- Sign in and allow access.

- Then You’ll see:
“The authentication flow has completed. You may close this window.”

---

### 6. Download the token.pickle File

- Now run a simple Python HTTP server to download the token from your mobile browser:

```
python3 -m http.server 8080
```
Visit `http://localhost:8080` in your Android browser (like Chrome), and download token.pickle directly.



---

### ✅ Done

You’ve successfully generated and saved token.pickle.
Use it in your projects to access Google APIs without re-authenticating.

