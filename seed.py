# import os
# import random
# import django
#
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'yugioh_django_proj.settings')
# django.setup()
#
# # After setup()
import requests

# from trading_cards.models import *

url = 'https://db.ygoprodeck.com/api/v7/cardinfo.php?name=Dark Magician'
response = requests.get(url)
card = response.json()
print(card)