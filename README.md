# 🥷 GhostRonin — Subdomain Recon & Classifier

GhostRonin is a Python-based reconnaissance tool for automating subdomain enumeration, filtering, status code categorization, and basic port scanning — all from one sleek command.
## 🚀 Features

- 🔍 Subdomain enumeration using `subfinder`, `assetfinder`, and `crt.sh`
- 🧹 Optional filtering of subdomains based on a specific root (e.g., `*.target.com`)
- ✅ Alive host detection with `httpx`
- 📊 Categorization of subdomains by HTTP status code
- 📂 Organized outputs for better readability and further use
- 🧠 Fully command-line ready (can be called as `ghostronin` from anywhere)

---

## ⚙️ Requirements

Make sure the following tools are installed and accessible from your `$PATH`:

- [`subfinder`](https://github.com/projectdiscovery/subfinder)
- [`assetfinder`](https://github.com/tomnomnom/assetfinder)
- [`httpx-toolkit`](https://www.kali.org/tools/httpx-toolkit/)
- `jq`, `curl`, and `sed` (default in most Linux distros)

---
### 🐍 Python Dependencies

To install required Python libraries:

1. (Optional but recommended) Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```
2. Install dependencies from requirements.txt:
```bash
pip install -r requirements.txt
```

## 📦 Installation
1. Clone the repository:
```bash
git clone https://github.com/mesbah-dev/ghostronin.git
cd ghostronin
```

2. (Optional) Install Python requirements if using a virtual environment:
```bash
pip install -r requirements.txt
```

4. Make it globally executable:
```bash
chmod +x ghostronin.py
sudo ln -s $(pwd)/ghostronin.py /usr/local/bin/ghostronin
```

---
## 🧪 Usage
`Basic usage:`
> ghostronin target.com

`Filter by subdomain root:`
> ghostronin target.com x.target.com

This will include only subdomains that end with x.target.com in the final scan list.

---
## 📁 Output Structure

| Structure | Description |
| ---------- | ------------------ |
| subfinder.txt | Results from subfinder |
| assetfinder.txt | Results from assetfinder  |
| all_subs.txt | Merged subdomain list  |
| alive.txt | Hosts responding to HTTP requests  |
| alive-info.txt | Detailed info from httpx-toolkit  |
| 200.txt | 2xx responses  |
| 300.txt | 3xx responses  |
| 400.txt | 4xx responses  |
| 500.txt | 5xx responses  |
---

## 🧠 Notes
- The banner is just for fun. Your recon is the real weapon 😉
- Make sure you don't abuse public targets. Respect all bug bounty program rules and scopes.

---

# 📄 License
MIT License. Free to use, share, and modify.
---
`Made with ❤️ by Tarnished`
