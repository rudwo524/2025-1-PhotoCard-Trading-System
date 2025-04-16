from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from django.shortcuts import render
from .models import CardMaster
import os
from django.conf import settings

def card_list(request):
    cards = CardMaster.objects.all()
    # image_dir = os.path.join(settings.MEDIA_ROOT, 'cards')
    # try:
    #     image_filenames = os.listdir(image_dir)
    #     image_urls = ['/media/cards/' + filename for filename in image_filenames]
    # except FileNotFoundError:
    #     image_urls = []
    # print(image_urls)
    return render(request, 'cards/card_list.html', {'cards': cards})