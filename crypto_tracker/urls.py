from django.contrib import admin
from django.urls import path, include
from tracker.views import index, generate_mnemonic_view, profile, show_mnemonics

urlpatterns = [
    path('admin/', admin.site.urls),
    path('generate-mnemonic/', generate_mnemonic_view, name='generate_mnemonic'),
    path('', index, name='index'),
    path('<int:wallet_id>/', index, name='wallet_detail'),
    path('profile/', profile, name='profile'),
    path('mnemonics/', show_mnemonics, name='show_mnemonics'),
]
