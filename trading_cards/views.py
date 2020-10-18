from django.shortcuts import render


def index(request):
    return render(request, 'trading_cards/index.html')
