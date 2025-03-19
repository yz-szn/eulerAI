import datetime
from colorama import Fore, Style, init

init(autoreset=True)

COLORS = {
    "EulerBOT": Fore.GREEN,
    "TIMESTAMP": Fore.CYAN,
}

def log(action, message):
    timestamp = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
    color_action = COLORS.get(action, Style.RESET_ALL)
    color_time = COLORS["TIMESTAMP"]
    
    # Default color
    processed_message = f"{Fore.WHITE}{message}"
    
    # Parsing khusus untuk multi-color
    if message.startswith(("[ Kirim Pesan ]", "[ Voting ]")):
        parts = message.split("]", 1)
        if len(parts) == 2:
            label = parts[0] + "]"
            status = parts[1].strip()
            status_color = Fore.GREEN if "SUKSES" in status else Fore.RED
            processed_message = f"{Fore.WHITE}{label} {status_color}{status}"
            
    elif message.startswith("[ Total Reward ]"):
        parts = message.split("]", 1)
        if len(parts) == 2:
            label = parts[0] + "]"
            value = parts[1].strip()
            processed_message = f"{Fore.WHITE}{label} {Fore.YELLOW}{value}"
            
    elif "Error occurred:" in message:
        processed_message = f"{Fore.RED}{message}"

    log_output = (
        f"{color_action}[ {action} ]{Style.RESET_ALL} "
        f"{color_time}[ {timestamp} ]{Style.RESET_ALL} "
        f"{processed_message}"
    )
    
    print(log_output)