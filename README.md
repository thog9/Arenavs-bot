# ArenaVS Bot Scripts 🚀

A collection of Python scripts to facilitate interaction with the ArenaVS platform, including login, task completion, and faucet requests on the testnet. Built with asyncio, aiohttp, web3.py, and designed for multi-wallet operation with multi-language support.

🔗 Register: [ArenaVS Whitelist](https://launchpad.arenavs.com/collections/bf4b9276-794c-43f1-bdc2-b7297c8d5568?ref-start=94a80706-0c21-4e3e-8cd5-a798cab62a5b)

## ✨ Features Overview

### General Features

- **Multi-Account Support**: Reads private keys or addresses from `pvkey.txt` or `address.txt` to perform actions across multiple accounts.
- **Colorful CLI**: Uses `colorama` for visually appealing output with colored text and borders.
- **Asynchronous Execution**: Built with `asyncio` for efficient network and task interactions.
- **Error Handling**: Comprehensive error catching for API requests and network issues.
- **Bilingual Support**: Supports both English and Vietnamese output based on user selection.
- **Proxy Support**: Optional proxy usage via `proxies.txt` for enhanced privacy and rate limiting.

### Included Scripts

1. **ArenaVS Task Automation**:
   - Auto login using private keys.
   - Fetch and complete tasks (e.g., social media follow, join Discord, etc.).
   - Supports proxy rotation for multiple accounts.

## 🛠️ Prerequisites

Before running the scripts, ensure you have the following installed:

- Python 3.8+
- `pip` (Python package manager)
- **Dependencies**: Install via `pip install -r requirements.txt` (ensure `web3.py`, `colorama`, `asyncio`, `eth-account`, `aiohttp_socks` and `inquirer` are included).
- **pvkey.txt**: Add private keys (one per line) for wallet automation.
- **proxies.txt** (optional): Add proxy addresses for network requests, if needed.


## 📦 Installation

1. **Clone this repository:**
- Open cmd or Shell, then run the command:
```sh
git clone https://github.com/thog9/Arenavs-bot.git
```
```sh
cd Arenavs-bot
```
2. **Install Dependencies:**
- Open cmd or Shell, then run the command:
```sh
pip install -r requirements.txt
```
3. **Prepare Input Files:**
- Open the `pvkey.txt`: Add your private keys (one per line) in the root directory.
```sh
nano pvkey.txt 
```

- Create `proxies.txt` for specific operations:
```sh
nano proxies.txt
```
4. **Run:**
- Open cmd or Shell, then run command:
```sh
python main.py
```
- Choose a language (Vietnamese/English).

## 📬 Contact
Connect with us for support or updates:

- **Telegram**: [thog099](https://t.me/thog099)
- **Channel**: [CHANNEL](https://t.me/thogairdrops)
- **Group**: [GROUP CHAT](https://t.me/thogchats)
- **X**: [Thog](https://x.com/thog099) 

----

## ☕ Support Us
Love these scripts? Fuel our work with a coffee!

🔗 BUYMECAFE: [BUY ME CAFE](https://buymecafe.vercel.app/)

