import os
import sys
import asyncio
from tools.eulerBOT import main as euler_main
from utils.logger import log
from colorama import init, Fore, Style

init(autoreset=True)

def welcome():
    print(
        f"""
        {Fore.GREEN + Style.BRIGHT}
         /$$   /$$ /$$$$$$$$        /$$$$$$$ /$$$$$$$$ /$$$$$$$             
        | $$  | $$|____ /$$/       /$$_____/|____ /$$/| $$__  $$            
        | $$  | $$   /$$$$/       |  $$$$$$    /$$$$/ | $$  \ $$            
        | $$  | $$  /$$__/         \____  $$  /$$__/  | $$  | $$           
        |  $$$$$$$ /$$$$$$$$       /$$$$$$$/ /$$$$$$$$| $$  | $$           
         \____  $$|________/      |_______/ |________/|__/  |__/           
        /$$  | $$ ______________________________________________                                                     
       |  $$$$$$/ ============ Nothing's Impossible !! =========                                       
        \______/
        """
    )

welcome()
print(f"{Fore.CYAN}{'=' * 18}")
print(Fore.CYAN + "#### EulerAI ####")
print(f"{Fore.CYAN}{'=' * 18}")

async def main():
    while True:
        print(Fore.YELLOW + "\n[=== PILIH MENU ===]")
        print(Fore.CYAN + "1. Jalankan EulerAI")
        print(Fore.CYAN + "2. Keluar")

        choice = input(Fore.GREEN + "Masukkan pilihan (1-2): ").strip()

        if choice == "1":
            print(Fore.BLUE + "Memulai program...")
            euler_main()
        elif choice == "2":
            print(Fore.RED + "Keluar dari program...")
            return
        else:
            print(Fore.RED + "Pilihan tidak valid! Mohon pilih antara 1-2.")

if __name__ == "__main__":
    asyncio.run(main())