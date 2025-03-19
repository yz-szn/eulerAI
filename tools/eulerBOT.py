import requests
import uuid
import json
import time
import random
import os
from colorama import Fore, Style, init
from utils.logger import log

init(autoreset=True)

BASE_URL = "https://dev.euler.ai/chat"
POINTS_URL = "https://dev.euler.ai/points/api/points/info"
HEADERS = {
    "Origin": "https://app.euler.ai",
    "Referer": "https://app.euler.ai/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
    "Content-Type": "application/json"
}

BLOCKCHAIN_TOPICS = [
    "Apa itu blockchain dan bagaimana cara kerjanya?",
    "Bagaimana blockchain dapat meningkatkan keamanan data?",
    "Apa perbedaan antara blockchain publik dan privat?",
    "Bagaimana smart contract bekerja di blockchain?",
    "Apa keuntungan menggunakan blockchain dalam industri keuangan?",
    "Bagaimana blockchain bisa digunakan dalam supply chain management?",
    "Apa tantangan utama dalam mengadopsi teknologi blockchain?",
    "Bagaimana consensus mechanism seperti Proof of Work dan Proof of Stake bekerja?",
    "Apa itu decentralized finance (DeFi) dan bagaimana kaitannya dengan blockchain?",
    "Bagaimana NFT (Non-Fungible Tokens) memanfaatkan teknologi blockchain?"
]

def read_accounts(filename="data/akun.txt"):
    accounts = []
    with open(filename, "r") as file:
        for line in file.read().splitlines():
            address, token = line.split(":")
            accounts.append({"address": address, "token": token})
    return accounts

def get_models(session_token):
    url = f"{BASE_URL}/models"
    headers = HEADERS.copy()
    headers["Authorization"] = f"Bearer {session_token}"
    response = requests.get(url, headers=headers)
    return response.json()

def multi_request(session_token, models, message):
    url = f"{BASE_URL}/multi"
    chat_id = str(uuid.uuid4())
    
    payload = {
        "chatId": chat_id,
        "history": [],
        "intent": message,
        "models": models,
        "session": session_token
    }
    
    headers = HEADERS.copy()
    headers["Authorization"] = f"Bearer {session_token}"
    
    response = requests.post(url, json=payload, headers=headers, stream=True)
    
    if response.status_code == 201:
        for line in response.iter_lines():
            if line:
                decoded_line = line.decode('utf-8')
                if decoded_line.startswith('data:'):
                    pass
    else:
        print(f"Error: {response.status_code}")
    
    return chat_id

def send_vote(session_token, chat_id, models, vote=1):
    url = f"{BASE_URL}/vote"
    
    payload = {
        "chatId": chat_id,
        "models": models,
        "vote": vote,
        "session": session_token
    }
    
    headers = HEADERS.copy()
    headers["Authorization"] = f"Bearer {session_token}"
    
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 201:
        try:
            response_data = response.json()
            if response_data.get("result") == "ok":
                return True
        except json.JSONDecodeError:
            pass
    return False

def get_points_info(address):
    params = {"address": address}
    response = requests.get(POINTS_URL, params=params, headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    return None

def main():
    accounts = read_accounts()
    selected_models = ["microsoft/phi-4", "microsoft/WizardLM-2-8x22B"]
    
    while True:
        for idx, account in enumerate(accounts):
            try:
                message = random.choice(BLOCKCHAIN_TOPICS)
                log("EulerBOT", f"[ Akun ] {account['address']}")
                log("EulerBOT", f"[ Pesan ] {message}")
                chat_id = multi_request(account['token'], selected_models, message)
                log("EulerBOT", "[ Kirim Pesan ] SUKSES")
                vote_success = send_vote(account['token'], chat_id, ["microsoft/WizardLM-2-8x22B"])
                if vote_success:
                    log("EulerBOT", "[ Voting ] SUKSES")
                else:
                    log("EulerBOT", "[ Voting ] GAGAL")
                
                points_info = get_points_info(account['address'])
                if points_info and points_info.get("code") == 0:
                    total_reward = points_info["data"]["total_reward"]
                    log("EulerBOT", f"[ Total Reward ] {total_reward} poin")
                else:
                    log("EulerBOT", "[ Total Reward ] GAGAL MENDAPATKAN INFO")
                
                time.sleep(5)
                
            except Exception as e:
                log("EulerBOT", f"Error occurred: {e}")
                continue

if __name__ == "__main__":
    main()