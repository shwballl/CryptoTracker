from django.db import models
from web3 import Web3
from eth_account import Account
from mnemonic import Mnemonic
import requests

ETHERSCAN_API_KEY = "GT4XMIQBJMFXDG7XIM5YD62WADW67KBF3I"
INFURA_URL = "https://mainnet.infura.io/v3/1ea31bc81d3a413789fee2a626f53167"
web3 = Web3(Web3.HTTPProvider(INFURA_URL))

Account.enable_unaudited_hdwallet_features()

class Mnemonic(models.Model):
    phrase = models.CharField(max_length=255)

    def create_wallet(self):
        account = Account.from_mnemonic(self.phrase)
        wallet = Wallet.objects.create(address=account.address, mnemonic=self)
        return wallet

    def get_balance(self, address):
        url = f"https://api.etherscan.io/api?module=account&action=balance&address={address}&apikey={ETHERSCAN_API_KEY}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            balance_wei = int(data.get("result", 0))
            balance_eth = Web3.from_wei(balance_wei, 'ether')
            balance, created = Balance.objects.get_or_create(address=address, defaults={'balance': balance_eth})
            if not created:
                balance.balance = balance_eth
                balance.save()
            return balance
        else:
            raise Exception("Ошибка при запросе баланса.")

    def __str__(self):
        return self.phrase

class Wallet(models.Model):
    address = models.CharField(max_length=42)
    mnemonic = models.ForeignKey(Mnemonic, on_delete=models.CASCADE)

    def __str__(self):
        return self.address

class Balance(models.Model):
    address = models.CharField(max_length=42)
    balance = models.DecimalField(max_digits=18, decimal_places=8)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.address
