# Cloudflared Tunnel Setup Guide

## Install Cloudflared

```bash
wget -O cloudflared.deb https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb && sudo dpkg -i cloudflared.deb && rm -f cloudflared.deb
```

---

# Login To Cloudflare

```bash
cloudflared tunnel login
```

This will open a browser window.

Select your domain and authorize Cloudflare.

---

# Create Tunnel

```bash
cloudflared tunnel create mytunnel
```

Example Output:

```text
Tunnel credentials written to /root/.cloudflared/e50636f7-c569-43c6-bb31-e1f72a87f3b6.json
Created tunnel mytunnel with id e50636f7-c569-43c6-bb31-e1f72a87f3b6
```

Copy the Tunnel ID:

```text
e50636f7-c569-43c6-bb31-e1f72a87f3b6
```

Cloudflared automatically creates:

```text
/root/.cloudflared/<TUNNEL-ID>.json
```

---

# Delete Tunnel

```bash
cloudflared tunnel delete mytunnel
```

Example:

```bash
cloudflared tunnel delete gkbotz.qzz.io
```

---

# If Tunnel Already Exists

Example Error:

```text
failed to create tunnel: Create Tunnel API call failed: tunnel with name already exists
```

List existing tunnels:

```bash
cloudflared tunnel list
```

Example:

```text
ID                                   NAME        CREATED
4a17924b-6517-4279-bfc3-e8fca32dd961 gkbotz      2026-05-16T06:57:54Z
ab327710-31f3-49b4-8c66-f4453b6c96e0 mytunnel    2026-04-29T07:33:47Z
```

Use the existing Tunnel ID directly.

---

# Create Required Directory

```bash
sudo mkdir -p /etc/cloudflared
```

---

# Start Your Apps First

Verify your applications are already running locally before starting Cloudflared.

Example:

```bash
curl http://127.0.0.1:8002
curl http://127.0.0.1:8080
curl http://127.0.0.1:8068
```

---

# Create config.yml

Open config file:

```bash
sudo nano /etc/cloudflared/config.yml
```

Example Configuration:

```yaml
tunnel: mytunnel
credentials-file: /root/.cloudflared/4a17924b-6517-4279-bfc3-e8fca32dd961.json

ingress:
  - hostname: tools.gkbotz.qzz.io
    service: http://127.0.0.1:8002

  - hostname: stream.gkbotz.qzz.io
    service: http://127.0.0.1:8080

  - hostname: preet.gkbotz.qzz.io
    service: http://127.0.0.1:8068

  - hostname: short.gkbotz.qzz.io
    service: http://127.0.0.1:3000

  - service: http_status:404
```

---

# Understanding The Config

## tunnel

```yaml
tunnel: mytunnel
```

Tunnel name created earlier.

---

## credentials-file

```yaml
credentials-file: /root/.cloudflared/<TUNNEL-ID>.json
```

Path to tunnel credentials file.

---

## ingress

Defines which domain points to which local app.

Example:

```yaml
- hostname: tools.gkbotz.qzz.io
  service: http://127.0.0.1:8002
```

Meaning:

```text
https://tools.gkbotz.qzz.io
            ↓
http://127.0.0.1:8002
```

---

# Add DNS Records

Create DNS routes for every subdomain:

```bash
cloudflared tunnel route dns mytunnel tools.gkbotz.qzz.io
cloudflared tunnel route dns mytunnel stream.gkbotz.qzz.io
cloudflared tunnel route dns mytunnel preet.gkbotz.qzz.io
cloudflared tunnel route dns mytunnel watch.gkbotz.qzz.io
cloudflared tunnel route dns mytunnel short.gkbotz.qzz.io
```

Cloudflare automatically creates required DNS records.

---

# Install Cloudflared Service

Run Cloudflared in background permanently:

```bash
sudo cloudflared --config /etc/cloudflared/config.yml service install
```

---

# Start And Enable Cloudflared

```bash
sudo systemctl start cloudflared
sudo systemctl enable cloudflared
```

---

# Verify Cloudflared Status

```bash
sudo systemctl status cloudflared
```

Expected Output:

```text
Active: active (running)
```

---

# Open In Browser

```text
https://tools.gkbotz.qzz.io
```

---

# Add New Apps Or Domains

## Edit Config

```bash
sudo nano /etc/cloudflared/config.yml
```

Add another ingress block:

```yaml
- hostname: watch.gkbotz.qzz.io
  service: http://127.0.0.1:9000
```

---

# Create DNS For New Domain

```bash
cloudflared tunnel route dns mytunnel watch.gkbotz.qzz.io
```

---

# Restart Cloudflared

```bash
sudo systemctl restart cloudflared
```

---

# Validate Config

```bash
cloudflared tunnel ingress validate
```

Expected Output:

```text
Validating rules from /etc/cloudflared/config.yml
OK
```

---

# Debug Tunnel Manually

```bash
cloudflared tunnel --config /etc/cloudflared/config.yml run mytunnel
```

Useful for checking startup errors directly in terminal.

---

# Common Error

## Credentials File Missing

Example Error:

```text
Tunnel credentials file '/root/.cloudflared/4a17924b-6517-4279-bfc3-e8fca32dd961.json' doesn't exist
```

Reason:
- Wrong Tunnel ID
- Deleted credentials file
- Wrong path in `credentials-file`

Fix:
- Verify file exists:

```bash
ls /root/.cloudflared/
```

- Update correct path in:

```bash
/etc/cloudflared/config.yml
```

---

# Uninstall Cloudflared Service

```bash
cloudflared service uninstall
```

---

# Recommended Practices

- Always use `127.0.0.1`
- Keep apps running locally first
- Validate config before restarting
- One tunnel can handle many domains/apps
- Never expose app ports publicly if using Cloudflared
- Keep `.json` credentials file secure

---

# Example Full Setup Flow

```text
Internet
    ↓
Cloudflare Tunnel
    ↓
tools.gkbotz.qzz.io
    ↓
127.0.0.1:8002
    ↓
Your App
```
