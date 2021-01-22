from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, HttpRequest
from django.views import generic, View
from django.utils import timezone
from django import forms
from .models import Board
import json


class IndexView(generic.ListView):
    template_name = 'index.html'
    context_object_name = 'board_list'

    def get_queryset(self):
        return Board.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')


class write(generic.TemplateView):
    template_name = 'write.html'


class Detail(generic.DetailView):
    template_name = 'detail.html'
    model = Board


def writeBoard(request):
    if request.method == 'POST':
        title = request.POST.get('title', 'None')
        context = request.POST.get('context', 'None')
        pub_date = timezone.now()
        board = Board(title=title, context=context, pub_date=pub_date)
        board.save()
    return HttpResponseRedirect('/pcsub')


def deleteBoard(request, pk):
    board = get_object_or_404(Board, pk=pk)
    board.delete()
    return HttpResponseRedirect('/pcsub')