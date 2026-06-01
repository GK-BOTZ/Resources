## CHECK AND UPDATE SYSTEM PACKAGES

```bash
sudo apt update -y && sudo apt upgrade -y
```


## INSTALL REQUIRED PACKAGES 

```bash
sudo apt install -y \
python3.12 \
python3-pip \
git \
nano \
zip \
unzip \
screen \
ffmpeg \
curl 
```

## Run This To Clean Unnecessary Files
```bash
sudo apt autoremove --purge -y
sudo apt clean
sudo apt autoclean
```

### Note: Aap Khudse Aur Packages Add Kar Sakte Hai.

Like: docker install ke liye.

```bash
sudo apt install docker.io
```

### Install NodeJS
```bash
curl -fsSL https://deb.nodesource.com/setup_lts.x | bash - && apt install -y nodejs
```



# HappyCoding
