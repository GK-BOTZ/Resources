Here you go — this is your final .md file content, exactly as requested, professional and streamlined:

### 🔽 README.md

## 🔐 Token Generator for Google OAuth (`token.pickle`)

This tool allows you to securely generate a `token.pickle` for accessing Google APIs (Drive, Gmail, YouTube, etc.) using `credentials.json`.

---

## 🚀 Setup Instructions

### 1. Install Termux (If Not Already Installed)

Download from the Play Store/App Store:  
➡️ [Play Store](https://play.google.com/store/apps/details?id=com.termux)
➡️ [App Store](https://apps.apple.com/in/app/termux/id6755708389)

Then open Termux and run:

--- 

```bash
apt update && apt upgrade -y
pkg install -y git python python-cryptography
pip install --upgrade pip
```

Install Google OAuth libraries:

```bash
pip install --upgrade google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

---

## ⚠️ Fix error: Installing pip is forbidden

If you get:

```
ERROR: Installing pip is forbidden
```

Run:

```bash
curl -sS https://bootstrap.pypa.io/get-pip.py | python
```

Then reinstall libraries:

```bash
pip install --upgrade google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

Reference:  
https://pip.pypa.io/en/stable/installation/

---


### 2. Fork This Repository

https://github.com/GK-BOTZ/Token-Pickle/fork

---

### 3. Upload Your Credentials File
Now Upload Your `json` File And name it `credentials.json`

--- 

### 4. Clone The Repo
```bash
git clone https://github.com/YOUR_USERNAME/Token-Pickle
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


## Testing token.pickle

Run This
```
python3 test_token_pickle.py
```

## Extract token.pickle Information To Use Anywhere 

Run This
```
python3 extract_token_pickle.py
```
