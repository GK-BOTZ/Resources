# 🚀 Generate Google Drive token.pickle, Client ID, Client Secret & Refresh Token

This guide explains how to generate a valid **Google OAuth 2.0 token (`token.pickle`)** and extract:

- ✅ Client ID  
- ✅ Client Secret  
- ✅ Refresh Token  

using **Android (Termux)** after Google’s new OAuth 2.0 security policy update.

These credentials can be used for:
- Cloudflare SecretX Index
- Drive OAuth scripts
- Google Drive API automation

---

## 🔗 Official References

- Google OAuth 2.0  
  https://developers.google.com/identity/protocols/oauth2  

- Google Drive API  
  https://developers.google.com/drive/api/v3/about-sdk  

- OAuth Client Credentials Guide  
  https://developers.google.com/workspace/guides/create-credentials  

- Termux (official)  
  https://f-droid.org/en/packages/com.termux/  

- Cloudflare Workers  
  https://developers.cloudflare.com/workers/  

- OAuth Native App Flow  
  https://developers.google.com/identity/protocols/oauth2/native-app  

- Refresh Token Docs  
  https://developers.google.com/identity/protocols/oauth2#offline  

- Google OAuth Security Policy  
  https://support.google.com/cloud/answer/9110914  

- Google OAuth Safety Update  
  https://developers.googleblog.com/2022/02/making-oauth-flows-safer.html  

---


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


## Credits :-
https://github.com/subhajit-maji/Gdrive-OAuth-Gen
