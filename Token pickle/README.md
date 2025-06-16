# Steps To Generate Token Pickle.


---

## Steps

### 1. Install Termux  
Download and install [Termux](https://github.com/termux/termux-app/releases).  

### 2. Set Up Termux  
Open Termux and run this command to update, install necessary packages, and set up Python:

```bash
pkg update && pkg upgrade -y && pkg install git python python-pip -y && python -m pip install --upgrade pip && pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

### 2. Clone the Repository (Directly in internal Storage)
First, Give Termux storage access:

```bash
termux-setup-storage
```

Now nevigate to the Internal Storage:

```bash
cd /sdcard
```

Run the following to clone the `TokenPickle` repository:

```bash
git clone https://github.com/rjriajul/TokenPickle
cd TokenPickle
```

### 3. Add `credentials.json`  

Then Move the `credentials.json` file to your phone’s internal storage.
```bash
cp /sdcard/credentials.json /data/data/com.termux/files/home/TokenPickle
```

### 4. Generate the Token  
Navigate to the project folder and run the script:

```bash
python3 generate_token.py
```

Copy the URL displayed, open it in a browser, and log in to your Google account. After successful authentication, you’ll see the message:  
**“The authentication flow has completed. You may close this window.”**

### 5. Save `token.pickle`  
Copy the generated token to your phone's storage:

```bash
cp token.pickle /sdcard
```

---

## Done! 🎉  
You’ll find `token.pickle` in your phone’s internal storage.  


## Credit

[`SilentDemonSD`](https://github.com/SilentDemonSD)
