from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from django.utils import timezone
from .models import Board

class IndexView(generic.ListView):
    template_name = 'index.html'
    context_object_name = 'board_list'

    def get_queryset(self):
        return Board.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]
