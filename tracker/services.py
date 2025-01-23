from web3 import Web3
import requests
from mnemonic import Mnemonic
from eth_account import Account

ETHERSCAN_API_KEY = "GT4XMIQBJMFXDG7XIM5YD62WADW67KBF3I"

INFURA_URL = "https://mainnet.infura.io/v3/1ea31bc81d3a413789fee2a626f53167" 
web3 = Web3(Web3.HTTPProvider(INFURA_URL))


def generate_mnemonic():
    mnemo = Mnemonic("english")
    return mnemo.generate(strength=128)

def create_wallet(mnemonic: str):
    account = Account.from_mnemonic(mnemonic)
    return {
        "address": account.address,
        "mnemonic": mnemonic
    }

def get_balance(address: str):
    url = f"https://api.etherscan.io/api?module=account&action=balance&address={address}&apikey={ETHERSCAN_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        balance_wei = int(data.get("result", 0))
        balance_eth = Web3.from_wei(balance_wei, 'ether')
        return balance_eth
    else:
        raise Exception("Ошибка при запросе баланса.")
