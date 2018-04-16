from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView

from OnmyojiSearch.models import Monster, Rarity


def index(request):
    return render(request, "OnmyojiSearch/index.html")


class IndexView(ListView):
    template_name = "OnmyojiSearch/index.html"
    model = Monster
    context_object_name = "monsters"
    rarity_kwargs = "rarity"

    def get_queryset(self):
        rarity = int(self.kwargs.get(self.rarity_kwargs, None))
        monsters = Monster.objects.all()
        if rarity > 0:
            monsters = get_object_or_404(Monster, rarity=rarity)
        return monsters

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        rarity = Rarity.objects.all()
        context["rarity"] = rarity
        context["i"] = 0
        return context





