import os
import sys
import asyncio
import random
from web3 import Web3
from eth_account import Account
from eth_account.messages import encode_defunct
from colorama import init, Fore, Style
from typing import List, Tuple, Dict
import aiohttp
from aiohttp_socks import ProxyConnector

# Initialize colorama
init(autoreset=True)

# Constants
API_BASE_URL = "https://launchpad-api.arenavs.com/api/v1"
IP_CHECK_URL = "https://api.ipify.org?format=json"
BORDER_WIDTH = 80
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5",
    "Origin": "https://launchpad.arenavs.com",
    "Referer": "https://launchpad.arenavs.com/",
    "Sec-Ch-Ua": '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": '"Windows"',
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-site",
}

# Configuration
CONFIG = {
    "DELAY_BETWEEN_ACCOUNTS": [5, 15],  # Seconds
    "RETRY_ATTEMPTS": 3,
    "RETRY_DELAY": 3,  # Seconds
    "MAX_CONCURRENCY": 5,
    "BYPASS_SSL": True,
}

# Bilingual vocabulary
LANG = {
    'vi': {
        'title': 'ARENAVS - ĐĂNG NHẬP VÀ HOÀN THÀNH NHIỆM VỤ',
        'info': 'Thông tin',
        'found': 'Tìm thấy',
        'wallets': 'ví',
        'processing_wallets': '⚙ ĐANG XỬ LÝ {count} VÍ',
        'logging_in': 'Đang đăng nhập...',
        'wallet_address': 'Địa chỉ ví',
        'login_success': '✅ Đăng nhập thành công!',
        'login_failure': '❌ Đăng nhập thất bại: {error}',
        'pausing': 'Tạm dừng',
        'seconds': 'giây',
        'completed': '🏁 HOÀN THÀNH: {successful}/{total} VÍ THÀNH CÔNG',
        'pvkey_not_found': '❌ File pvkey.txt không tồn tại',
        'pvkey_empty': '❌ Không tìm thấy private key hợp lệ',
        'pvkey_error': '❌ Không thể đọc pvkey.txt',
        'invalid_key': 'không hợp lệ, đã bỏ qua',
        'warning_line': 'Cảnh báo: Dòng',
        'no_proxies': '❌ Không tìm thấy proxy trong proxies.txt',
        'found_proxies': '✅ Tìm thấy {count} proxy trong proxies.txt',
        'using_proxy': '🔄 Sử dụng Proxy - [{proxy}] với IP công khai - [{public_ip}]',
        'no_proxy': 'Không có proxy',
        'unknown': 'Không xác định',
        'ip_check_failed': '⚠ Không thể kiểm tra IP công khai: {error}',
        'fetching_tasks': 'Đang lấy danh sách nhiệm vụ...',
        'no_tasks': '❌ Không tìm thấy nhiệm vụ nào: {reason}',
        'tasks_found': '✅ Tìm thấy {count} nhiệm vụ:\n  - Hoàn thành: {completed} nhiệm vụ\n  - Chưa hoàn thành: {pending} nhiệm vụ',
        'completing_task': 'Đang thực hiện nhiệm vụ!',
        'task_success': '✅ Hoàn thành nhiệm vụ!\n  - Nhiệm vụ: {task_name}\n  - ID: {task_id}',
        'task_failure': '❌ Nhiệm vụ thất bại: {error}!\n  - Nhiệm vụ: {task_name}\n  - ID: {task_id}\n  - Chi tiết: {error_detail}',
        'message_to_sign': 'Message to sign: {message}',
        'generated_signature': 'Generated signature: {signature}',
        'sign_success': 'Message to sign thành công!',
    },
    'en': {
        'title': 'ARENAVS - LOGIN AND COMPLETE TASKS',
        'info': 'Info',
        'found': 'Found',
        'wallets': 'wallets',
        'processing_wallets': '⚙ PROCESSING {count} WALLETS',
        'logging_in': 'Logging in...',
        'wallet_address': 'Wallet address',
        'login_success': '✅ Login successful!',
        'login_failure': '❌ Login failed: {error}',
        'pausing': 'Pausing',
        'seconds': 'seconds',
        'completed': '🏁 COMPLETED: {successful}/{total} WALLETS SUCCESSFULLY',
        'pvkey_not_found': '❌ pvkey.txt file not found',
        'pvkey_empty': '❌ No valid private keys found',
        'pvkey_error': '❌ Failed to read pvkey.txt',
        'invalid_key': 'is invalid, skipped',
        'warning_line': 'Warning: Line',
        'no_proxies': '❌ No proxies found in proxies.txt',
        'found_proxies': '✅ Found {count} proxies in proxies.txt',
        'using_proxy': '🔄 Using Proxy - [{proxy}] with Public IP - [{public_ip}]',
        'no_proxy': 'None',
        'unknown': 'Unknown',
        'ip_check_failed': '⚠ Failed to check public IP: {error}',
        'fetching_tasks': 'Fetching tasks list...',
        'no_tasks': '❌ No tasks found: {reason}',
        'tasks_found': '✅ Found {count} tasks:\n  - Completed: {completed} tasks\n  - Pending: {pending} tasks',
        'completing_task': 'Processing task!',
        'task_success': '✅ Task completed!\n  - Task: {task_name}\n  - ID: {task_id}',
        'task_failure': '❌ Task failed: {error}!\n  - Task: {task_name}\n  - ID: {task_id}\n  - Detail: {error_detail}',
        'message_to_sign': 'Message to sign: {message}',
        'generated_signature': 'Generated signature: {signature}',
        'sign_success': 'Message to sign successful!',
    }
}

# Display functions
def print_border(text: str, color=Fore.CYAN, width=BORDER_WIDTH):
    text = text.strip()
    if len(text) > width - 4:
        text = text[:width - 7] + "..."
    padded_text = f" {text} ".center(width - 2)
    print(f"{color}┌{'─' * (width - 2)}┐{Style.RESET_ALL}", flush=True)
    print(f"{color}│{padded_text}│{Style.RESET_ALL}", flush=True)
    print(f"{color}└{'─' * (width - 2)}┘{Style.RESET_ALL}", flush=True)

def print_separator(color=Fore.MAGENTA):
    print(f"{color}{'═' * BORDER_WIDTH}{Style.RESET_ALL}", flush=True)

def print_message(message: str, color=Fore.YELLOW):
    print(f"{color}  > {message}{Style.RESET_ALL}", flush=True)

def print_wallets_summary(count: int, language: str = 'vi'):
    print_border(
        LANG[language]['processing_wallets'].format(count=count),
        Fore.MAGENTA
    )
    print()

# Utility functions
def is_valid_private_key(key: str) -> bool:
    key = key.strip()
    if not key.startswith('0x'):
        key = '0x' + key
    try:
        bytes.fromhex(key.replace('0x', ''))
        return len(key) == 66
    except ValueError:
        return False

def load_private_keys(file_path: str = "pvkey.txt", language: str = 'vi') -> List[Tuple[int, str]]:
    try:
        if not os.path.exists(file_path):
            print(f"{Fore.RED}  ✖ {LANG[language]['pvkey_not_found']}{Style.RESET_ALL}", flush=True)
            with open(file_path, 'w') as f:
                f.write("# Add private keys here, one per line\n# Example: 0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef\n")
            sys.exit(1)
        
        valid_keys = []
        with open(file_path, 'r') as f:
            for i, line in enumerate(f, 1):
                key = line.strip()
                if key and not key.startswith('#'):
                    if is_valid_private_key(key):
                        if not key.startswith('0x'):
                            key = '0x' + key
                        valid_keys.append((i, key))
                    else:
                        print(f"{Fore.YELLOW}  ⚠ {LANG[language]['warning_line']} {i} {LANG[language]['invalid_key']}: {key}{Style.RESET_ALL}", flush=True)
        
        if not valid_keys:
            print(f"{Fore.RED}  ✖ {LANG[language]['pvkey_empty']}{Style.RESET_ALL}", flush=True)
            sys.exit(1)
        
        return valid_keys
    except Exception as e:
        print(f"{Fore.RED}  ✖ {LANG[language]['pvkey_error']}: {str(e)}{Style.RESET_ALL}", flush=True)
        sys.exit(1)

def load_proxies(file_path: str = "proxies.txt", language: str = 'vi') -> List[str]:
    try:
        if not os.path.exists(file_path):
            print(f"{Fore.YELLOW}  ⚠ {LANG[language]['no_proxies']}. Using no proxy.{Style.RESET_ALL}", flush=True)
            with open(file_path, 'w') as f:
                f.write("# Add proxies here, one per line\n# Example: socks5://user:pass@host:port or http://host:port\n")
            return []
        
        proxies = []
        with open(file_path, 'r') as f:
            for line in f:
                proxy = line.strip()
                if proxy and not line.startswith('#'):
                    proxies.append(proxy)
        
        if not proxies:
            print(f"{Fore.YELLOW}  ⚠ {LANG[language]['no_proxies']}. Using no proxy.{Style.RESET_ALL}", flush=True)
            return []
        
        print(f"{Fore.YELLOW}  ℹ {LANG[language]['found_proxies'].format(count=len(proxies))}{Style.RESET_ALL}", flush=True)
        return proxies
    except Exception as e:
        print(f"{Fore.RED}  ✖ {LANG[language]['pvkey_error']}: {str(e)}{Style.RESET_ALL}", flush=True)
        return []

async def get_proxy_ip(proxy: str = None, language: str = 'vi') -> str:
    try:
        if proxy:
            if proxy.startswith(('socks5://', 'socks4://', 'http://', 'https://')):
                connector = ProxyConnector.from_url(proxy)
            else:
                parts = proxy.split(':')
                if len(parts) == 4:  # host:port:user:pass
                    proxy_url = f"socks5://{parts[2]}:{parts[3]}@{parts[0]}:{parts[1]}"
                    connector = ProxyConnector.from_url(proxy_url)
                elif len(parts) == 3 and '@' in proxy:  # user:pass@host:port
                    connector = ProxyConnector.from_url(f"socks5://{proxy}")
                else:
                    print(f"{Fore.YELLOW}  ⚠ Invalid proxy format: {proxy}{Style.RESET_ALL}", flush=True)
                    return LANG[language]['unknown']
            async with aiohttp.ClientSession(connector=connector, timeout=aiohttp.ClientTimeout(total=10)) as session:
                async with session.get(IP_CHECK_URL, headers=HEADERS) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get('ip', LANG[language]['unknown'])
                    print(f"{Fore.YELLOW}  ⚠ {LANG[language]['ip_check_failed'].format(error=f'HTTP {response.status}')}{Style.RESET_ALL}", flush=True)
                    return LANG[language]['unknown']
        else:
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=10)) as session:
                async with session.get(IP_CHECK_URL, headers=HEADERS) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get('ip', LANG[language]['unknown'])
                    print(f"{Fore.YELLOW}  ⚠ {LANG[language]['ip_check_failed'].format(error=f'HTTP {response.status}')}{Style.RESET_ALL}", flush=True)
                    return LANG[language]['unknown']
    except Exception as e:
        print(f"{Fore.YELLOW}  ⚠ {LANG[language]['ip_check_failed'].format(error=str(e))}{Style.RESET_ALL}", flush=True)
        return LANG[language]['unknown']

async def login(w3: Web3, private_key: str, wallet_index: int, language: str = 'vi', proxy: str = None) -> tuple[str, str]:
    print_border(f"Wallet {wallet_index}", Fore.YELLOW)
    print_message(LANG[language]['logging_in'], Fore.CYAN)
    
    address = Account.from_key(private_key).address
    print_message(f"  - {LANG[language]['wallet_address']}: {address}", Fore.YELLOW)
    public_ip = await get_proxy_ip(proxy, language)
    proxy_display = proxy if proxy else LANG[language]['no_proxy']
    print_message(f"  - {LANG[language]['using_proxy'].format(proxy=proxy_display, public_ip=public_ip)}", Fore.CYAN)

    for attempt in range(CONFIG['RETRY_ATTEMPTS']):
        try:
            connector = ProxyConnector.from_url(proxy) if proxy and proxy.startswith(('socks5://', 'socks4://', 'http://', 'https://')) else None
            async with aiohttp.ClientSession(connector=connector, timeout=aiohttp.ClientTimeout(total=30)) as session:
                # Get signature message
                url = f"{API_BASE_URL}/users/generate-signature-message/{address}"
                async with session.get(url, headers=HEADERS, ssl=not CONFIG['BYPASS_SSL']) as response:
                    if response.status != 200:
                        print_message(f"  - {LANG[language]['login_failure'].format(error=f'HTTP {response.status}')}", Fore.RED)
                        continue
                    data = await response.json()
                    message = data.get('message')
                    if not message:
                        print_message(f"  - {LANG[language]['login_failure'].format(error='No message received')}", Fore.RED)
                        continue
                    print_message(f"  - {LANG[language]['message_to_sign'].format(message=message)}", Fore.YELLOW)
                
                # Sign message
                message_hash = encode_defunct(text=message)
                signed_message = w3.eth.account.sign_message(message_hash, private_key=private_key)
                signature = "0x" + signed_message.signature.hex()
                print_message(f"  - {LANG[language]['generated_signature'].format(signature=signature)}", Fore.YELLOW)
                print_message(f"  - {LANG[language]['sign_success']}", Fore.GREEN)

                # Initialize user
                payload = {"walletAddress": address, "signature": signature}
                async with session.post(
                    f"{API_BASE_URL}/users/initialize",
                    headers=HEADERS,
                    json=payload,
                    ssl=not CONFIG['BYPASS_SSL']
                ) as response:
                    if response.status == 201:
                        data = await response.json()
                        token = data.get("token")
                        if token:
                            token_prefix = token.split('.')[0]  # Lấy phần đầu đến dấu chấm đầu tiên
                            print_message(f"  - {LANG[language]['login_success']}", Fore.GREEN)
                            print_message(f"    - Địa chỉ: {address}", Fore.YELLOW)
                            print_message(f"    - JWT: {token_prefix}", Fore.YELLOW)
                            return address, token
                        else:
                            print_message(f"  - {LANG[language]['login_failure'].format(error='No token received')}", Fore.RED)
                    else:
                        error_msg = await response.text()
                        print_message(f"  - {LANG[language]['login_failure'].format(error=f'HTTP {response.status}: {error_msg}')}", Fore.RED)
        except Exception as e:
            if attempt < CONFIG['RETRY_ATTEMPTS'] - 1:
                delay = CONFIG['RETRY_DELAY']
                print_message(f"  - {LANG[language]['login_failure'].format(error=str(e))}", Fore.RED)
                print_message(f"  - {LANG[language]['pausing']} {delay:.2f} {LANG[language]['seconds']}", Fore.YELLOW)
                await asyncio.sleep(delay)
                continue
            print_message(f"  - {LANG[language]['login_failure'].format(error=str(e))}", Fore.RED)
            return address, ""
    return address, ""

async def fetch_and_complete_tasks(token: str, language: str = 'vi', proxy: str = None) -> bool:
    print_message(LANG[language]['fetching_tasks'], Fore.CYAN)
    for attempt in range(CONFIG['RETRY_ATTEMPTS']):
        try:
            connector = ProxyConnector.from_url(proxy) if proxy and proxy.startswith(('socks5://', 'socks4://', 'http://', 'https://')) else None
            async with aiohttp.ClientSession(connector=connector, timeout=aiohttp.ClientTimeout(total=30)) as session:
                headers = HEADERS.copy()
                headers["Authorization"] = f"Bearer {token}"
                
                # Thử lấy danh sách nhiệm vụ từ /users/projects
                async with session.get(
                    f"{API_BASE_URL}/users/projects",
                    headers=headers,
                    ssl=not CONFIG['BYPASS_SSL']
                ) as response:
                    if response.status != 200:
                        print_message(f"  - {LANG[language]['task_failure'].format(task_name='Fetch projects', error=f'HTTP {response.status}', error_detail=f'HTTP {response.status}')}", Fore.RED)
                        continue
                    projects = await response.json()
                    
                    if not projects:
                        print_message(f"  - {LANG[language]['no_tasks'].format(reason='Không tìm thấy project')}", Fore.RED)
                        return False
                    
                    tasks = []
                    completed_task_ids = set()
                    for project in projects:
                        project_data = project.get('project')
                        if project_data and isinstance(project_data, dict):
                            project_tasks = project_data.get('tasks', [])
                            tasks.extend(project_tasks)
                            for completed_task in project_data.get('completedTasks', []):
                                task_id = completed_task.get('task', {}).get('id')
                                if task_id:
                                    completed_task_ids.add(task_id)
                        else:
                            print_message(f"    - ⚠ Dữ liệu project không hợp lệ: {project}", Fore.YELLOW)
                    
                    if not tasks:
                        print_message(f"  - {LANG[language]['no_tasks'].format(reason='Không tìm thấy nhiệm vụ trong project')}", Fore.RED)
                        return False
                    
                    print_message(
                        LANG[language]['tasks_found'].format(count=len(tasks), completed=len(completed_task_ids), pending=len(tasks) - len(completed_task_ids)),
                        Fore.GREEN
                    )

                    success = False
                    for task in tasks:
                        task_id = task.get('id')
                        task_name = task.get('taskName', 'Unknown Task')
                        if not task_id:
                            print_message(f"    - ⚠ Nhiệm vụ không có ID: {task_name}", Fore.YELLOW)
                            continue
                        print_message(f"  - {LANG[language]['completing_task']}", Fore.CYAN)
                        if task_id in completed_task_ids:
                            print_message(
                                f"    - {LANG[language]['task_failure'].format(
                                    task_name=task_name,
                                    task_id=task_id,
                                    error='Task already completed',
                                    error_detail='HTTP 400: Task already completed'
                                )}",
                                Fore.YELLOW
                            )
                            continue
                        async with session.post(
                            f"{API_BASE_URL}/tasks/{task_id}/complete",
                            headers=headers,
                            json={},
                            ssl=not CONFIG['BYPASS_SSL']
                        ) as task_response:
                            if task_response.status in (200, 201):
                                print_message(
                                    f"    - {LANG[language]['task_success'].format(task_name=task_name, task_id=task_id)}",
                                    Fore.GREEN
                                )
                                success = True
                            elif task_response.status == 400:
                                error_data = await task_response.json()
                                error_msg = error_data.get('message', 'Unknown error')
                                print_message(
                                    f"    - {LANG[language]['task_failure'].format(
                                        task_name=task_name,
                                        task_id=task_id,
                                        error=error_msg,
                                        error_detail=f'HTTP {task_response.status}: {error_msg}'
                                    )}",
                                    Fore.RED
                                )
                            else:
                                error_msg = await task_response.text()
                                print_message(
                                    f"    - {LANG[language]['task_failure'].format(
                                        task_name=task_name,
                                        task_id=task_id,
                                        error='Unknown error',
                                        error_detail=f'HTTP {task_response.status}: {error_msg}'
                                    )}",
                                    Fore.RED
                                )
                            await asyncio.sleep(1)  # Delay between tasks
                    return success
        except Exception as e:
            if attempt < CONFIG['RETRY_ATTEMPTS'] - 1:
                delay = CONFIG['RETRY_DELAY']
                print_message(f"  - {LANG[language]['task_failure'].format(task_name='Fetch projects', error=str(e), error_detail=str(e))}", Fore.RED)
                print_message(f"  - {LANG[language]['pausing']} {delay:.2f} {LANG[language]['seconds']}", Fore.YELLOW)
                await asyncio.sleep(delay)
                continue
            print_message(f"  - {LANG[language]['task_failure'].format(task_name='Fetch projects', error=str(e), error_detail=str(e))}", Fore.RED)
            return False
    return False

async def process_wallet(index: int, profile_num: int, private_key: str, proxy: str, language: str) -> tuple[str, str, bool]:
    w3 = Web3()  # Initialize Web3 without provider for signing
    address, token = await login(w3, private_key, profile_num, language, proxy)
    
    if not token:
        print_message(f"  - ✖ Skipping wallet {profile_num} due to login failure", Fore.RED)
        return address, "", False
    
    # Complete tasks
    tasks_success = await fetch_and_complete_tasks(token, language, proxy)
    return address, token, tasks_success

async def run_arenavs(language: str = 'vi'):
    print()
    print_border(LANG[language]['title'], Fore.CYAN)
    print()

    private_keys = load_private_keys('pvkey.txt', language)
    proxies = load_proxies('proxies.txt', language)
    random.shuffle(private_keys)
    print(f"{Fore.YELLOW}  ℹ {LANG[language]['info']}: {LANG[language]['found']} {len(private_keys)} {LANG[language]['wallets']}{Style.RESET_ALL}", flush=True)
    print()

    if not private_keys:
        return

    print_separator()

    print_wallets_summary(len(private_keys), language)

    successful_wallets = 0
    CONFIG['TOTAL_WALLETS'] = len(private_keys)
    CONFIG['MAX_CONCURRENCY'] = min(CONFIG['MAX_CONCURRENCY'], len(private_keys))

    async def limited_task(index, profile_num, private_key, proxy):
        nonlocal successful_wallets
        async with semaphore:
            address, token, success = await process_wallet(index, profile_num, private_key, proxy, language)
            if token and success:
                successful_wallets += 1
            if index < len(private_keys) - 1:
                delay = random.uniform(CONFIG['DELAY_BETWEEN_ACCOUNTS'][0], CONFIG['DELAY_BETWEEN_ACCOUNTS'][1])
                print_message(f"  - {LANG[language]['pausing']} {delay:.2f} {LANG[language]['seconds']}", Fore.YELLOW)
                await asyncio.sleep(delay)

    semaphore = asyncio.Semaphore(CONFIG['MAX_CONCURRENCY'])
    tasks = []
    for i, (profile_num, private_key) in enumerate(private_keys):
        proxy = proxies[i % len(proxies)] if proxies else None
        tasks.append(limited_task(i, profile_num, private_key, proxy))

    await asyncio.gather(*tasks, return_exceptions=True)

    print()
    print_border(f"{LANG[language]['completed'].format(successful=successful_wallets, total=len(private_keys))}", Fore.GREEN)
    print()

if __name__ == "__main__":
    asyncio.run(run_arenavs('vi'))
