from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('create_trade/<int:card_id>', views.make_trade, name='make_trade'),
    path('make_offer/<int:trade_id>', views.MakeOfferView.as_view(), name='make_offer')
]