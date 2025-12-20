# • Screen Commands :-

#### Create a Named Session
```bash
screen -S name
```

---

#### List All Sessions
```bash
screen -ls
```

---

#### Reattach to a Session
```bash
screen -r name
```

---

#### Detach Elsewhere and Reattach Here (Forcefully)
```bash
screen -r -d name
```
---

#### Kill a Specific Session
```bash
screen -X -S name quit
```
---

#### Remove Dead Sessions
```bash
screen -wipe
```
---

#### Kill All Screen
```bash
pkill screen
```
---

