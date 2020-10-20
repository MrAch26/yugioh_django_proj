from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from trading_cards.forms import MakeOfferForm
from trading_cards.models import Card, Trade, Offer


def index(request):
    trades = Trade.objects.filter(status='P')
    return render(request, 'trading_cards/index.html', {'trades': trades})


def make_trade(request, card_id):
    card = Card.objects.get(pk=card_id)
    if card not in request.user.profile.deck.all():
        # todo: add flash message - card does not belong for trade
        return redirect('home')

    trade = Trade.objects.create(
        card=card,
        profile=request.user.profile
    )
    # todo: message - trade successful (class Success, Danger) Toast materialize
    return redirect('home')


class MakeOfferView(CreateView):
    model = Offer
    form_class = MakeOfferForm

    # template_name = ''

    def form_valid(self, form):
        trade = Trade.objects.get(id=self.kwargs['trade_id'])
        offer = form.save(commit=False)
        offer.profile = self.request.user.profile
        offer.trade = trade
        offer.save()
        return redirect(reverse_lazy('home'))

    def get_context_data(self, **kwargs):
        context = super(MakeOfferView, self).get_context_data(**kwargs)
        form = MakeOfferForm()
        form.fields['card'].queryset = self.request.user.profile.deck.all()
        context['form'] = form
        trade = Trade.objects.get(id=self.kwargs['trade_id'])
        context['trade'] = trade
        return context