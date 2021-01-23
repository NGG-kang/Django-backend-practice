from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, HttpRequest
from django.views import generic, View
from django.utils import timezone
from django.contrib import messages
from django.shortcuts import redirect

from django import forms
from .models import Board
import json


class IndexView(generic.ListView):
    template_name = 'pcsub/index.html'
    context_object_name = 'board_list'

    def get_queryset(self):
        return Board.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]



class write(generic.TemplateView):
    template_name = 'pcsub/write.html'


class Detail(generic.DetailView):
    template_name = 'pcsub/detail.html'
    model = Board


class Modify(generic.DetailView):
    template_name = 'pcsub/modify.html'
    model = Board


def writeBoard(request):
    if request.method == 'POST':
        title = request.POST.get('title', 'None')
        context = request.POST.get('context', 'None')
        pub_date = timezone.now()
        board = Board()
        board.title = title
        board.context = context
        board.pub_date = pub_date
        board.author = request.user
        board.save()
    return HttpResponseRedirect('/pcsub')


def deleteBoard(request, pk):
    board = get_object_or_404(Board, pk=pk)
    if request.user != board.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('pcsub:detail', pk=board.id)
    else:
        board.delete()
    return HttpResponseRedirect('/pcsub')

def modifyBoard(request, pk):
    board= get_object_or_404(Board, pk=pk)
    if request.user != board.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('pcsub:modify', pk=board.id)
    if request.method == 'POST':
        title = request.POST.get('title', 'None')
        context = request.POST.get('context', 'None')
        pub_date = timezone.now()
        board.title = title
        board.context = context
        board.pub_date = pub_date
        board.author = request.user
        board.save()
    return redirect('pcsub:detail', pk=board.id)