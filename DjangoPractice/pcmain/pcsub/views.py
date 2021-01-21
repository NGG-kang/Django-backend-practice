from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views import generic, View
from django.utils import timezone
from .models import Board
import json


class IndexView(generic.ListView):
    template_name = 'index.html'
    context_object_name = 'board_list'

    def get_queryset(self):
        return Board.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]


class write(generic.TemplateView):
    template_name = 'write.html'


class Detail(generic.View):
    template_name = 'detail.html'
    context_object_name = 'board_list'

    def get_queryset(self):
        return Board.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]


def writeBoard(request):
    title = request.POST.get('title')
    context = request.POST.get('context')
    pub_date = timezone.now()
    board = Board(title=title, context=context, pub_date=pub_date)
    board.save()
    return HttpResponseRedirect('/pcsub')
