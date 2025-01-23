from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse

from .services import generate_mnemonic
from .models import Wallet, Balance
from tracker.models import Mnemonic

def generate_mnemonic_view(request):
    mnemonic_phrase = generate_mnemonic()
    mnemonic = Mnemonic.objects.create(phrase=mnemonic_phrase)
    wallet = mnemonic.create_wallet()
    balance = mnemonic.get_balance(wallet.address)
    return JsonResponse({
        "mnemonic": mnemonic.phrase,
        "wallet_address": wallet.address,
        "wallet_id": wallet.id,
        "balance": str(balance.balance)
    })

def show_mnemonics(request):
    mnemonics = Mnemonic.objects.all()
    context = {
        'mnemonics': mnemonics
    }
    return render(request, 'show_mnemonics.html', context)

def index(request, wallet_id=None):
    if wallet_id:
        wallet = get_object_or_404(Wallet, id=wallet_id)
    else:
        wallet = Wallet.objects.latest('id')

    balance = Balance.objects.filter(address=wallet.address).latest('id')


    previous_wallet = Wallet.objects.filter(id__lt=wallet.id).order_by('-id').first()
    next_wallet = Wallet.objects.filter(id__gt=wallet.id).order_by('id').first()

    context = {
        'balance': f"{balance.balance:.2f}",
        'address': wallet.address,
        'previous_wallet': previous_wallet,
        'next_wallet': next_wallet,
    }

    return render(request, 'index.html', context)

def profile(request):
    
    return render(request, 'account.html')