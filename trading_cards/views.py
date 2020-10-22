from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, DeleteView, UpdateView
from trading_cards.forms import MakeOfferForm
from trading_cards.models import Card, Trade, Offer

# class OwnerProtectMixin(object):
#     def dispatch(self, request, *args, **kwargs):
#         objectUser = self.get_object()
#         if objectUser.user != self.request.user:
#             return HttpResponseForbidden()
#         return super(OwnerProtectMixin, self).dispatch(request, *args, **kwargs)

def index(request):
    trades = Trade.objects.filter(status='P').order_by('-timestamp')
    return render(request, 'trading_cards/index.html', {'trades': trades})


def index_history(request):
    trades = Trade.objects.filter(status='F').order_by('-timestamp')
    return render(request, 'trading_cards/indexHistory.html', {'trades': trades})


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

@method_decorator(login_required, name='dispatch')
class MakeOfferView(CreateView):
    model = Offer
    form_class = MakeOfferForm

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
        context['edit'] = False
        return context

@method_decorator(login_required, name='dispatch')
def AcceptOffer(request, id, accepted):
    trade = Trade.objects.all()
    offer = Offer.objects.all()

    if accepted:
        offer.status = "A"
        trade.status = 'F'
        offer.deck.card


# OFFERS
@method_decorator(login_required, name='dispatch')
class OfferView(ListView):
    model = Offer
    context_object_name = 'offers'

@method_decorator(login_required, name='dispatch')
class UpdateOffer(UpdateView):
    model = Offer
    fields = ['card']
    context_object_name = 'offers'
    success_url = reverse_lazy('my_offer')

    def get_context_data(self, **kwargs):
        context = super(UpdateOffer, self).get_context_data(**kwargs)
        context['edit'] = True
        return context

@method_decorator(login_required, name='dispatch')
class DeleteOffer(DeleteView):
    model = Offer
    context_object_name = 'offers'
    success_url = reverse_lazy('home')


# TRANSACTIONS
@method_decorator(login_required, name='dispatch')
class TradeView(ListView):
    model = Trade
    context_object_name = 'trades'
    # template_name = 'trading_cards/trade_list.html'

