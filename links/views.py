import base64
import datetime
import hashlib
import json

from django.conf import settings
from django.http import JsonResponse, HttpResponsePermanentRedirect
from django.shortcuts import render, redirect
from django.utils import timezone

from .models import ShortURL, Viewer

#
BASE_URL = 'http://localhost:8001/links/'
BASE_SHORT_URL = 'http://localhost:8001/u/'

# hash salt when generate permanent url
HASH_SALT = 'meow'

# give default value when you create_302
DEFAULT_NAME = ''
DEFAULT_TITLE = ''
DEFAULT_DESCRIPTION = ''


def index(request):
    if request.method == 'GET':
        context = {
            'BASE_URL': BASE_URL,
            'BASE_SHORT_URL': BASE_SHORT_URL,
            'status': 'normal',
            'recent': ShortURL.objects.all().order_by('-id'),
        }
        return render(request, 'links/links.html', context)


def create_301(request):
    if request.method == "POST":
        target = request.POST.get('target')

        # error message
        if not target.startswith('http://') and not target.startswith('https://'):
            context = {
                'status': 400, 'msg': 'Target url must to starts with "http://" or "https://"'}
            return JsonResponse(context)

        # ==== Create objects ====
        shortcut = ShortURL.objects.create(
            mode=301,
            target=target
        )

        # generate permanent url
        # object id -> hash() -> [:6]
        # BE CAREFUL! it is possible to have collision
        permanent_url = base64.b64encode(
            hashlib.md5((str(shortcut.id) + HASH_SALT).encode('utf-8')).digest(), altchars=b"-_")[:6].decode("utf-8")
        shortcut.permanent_url = permanent_url
        shortcut.save()

        context = {'status': 200, 'permanent_url': permanent_url}
        return JsonResponse(context)


def create_302(request):
    if request.method == "POST":
        # ajax form input
        name = request.POST.get('name') if request.POST.get(
            'name') else DEFAULT_NAME
        target = request.POST.get('target')
        title = request.POST.get('title') if request.POST.get(
            'title') else DEFAULT_TITLE
        description = request.POST.get('description') if request.POST.get(
            'description') else DEFAULT_DESCRIPTION

        # error message
        if not target.startswith('http://') and not target.startswith('https://'):
            context = {
                'status': 400, 'msg': 'Target url must to starts with "http://" or "https://"'}
            return JsonResponse(context)

        # ==== Create object ====
        shortcut = ShortURL.objects.create(
            mode=302,
            name=name,
            target=target,
            title=title,
            description=description,
        )

        # generate permanent url
        # object id -> hash() -> [:6]
        # BE CAREFUL! it is possible to have collision
        permanent_url = base64.b64encode(
            hashlib.md5((str(shortcut.id) + HASH_SALT).encode('utf-8')).digest(), altchars=b"-_")[:6].decode("utf-8")
        shortcut.permanent_url = permanent_url
        shortcut.save()

        # save thumbnail image
        if request.FILES:
            shortcut.thumbnail.save(
                str(request.FILES['file']), request.FILES['file'], save=True)

        context = {
            'status': 200,
            'permanent_url': permanent_url,
            'name': name,
            'target': target,
            'title': title,
            'description': description,
            'thumbnail': (MEDIA_URL + str(shortcut.thumbnail) if shortcut.thumbnail else (settings.STATIC_URL + '/images/default_thumbnail.png')),
        }
        return JsonResponse(context)


def custom_url(request, custom_url):
    if ShortURL.objects.filter(name=custom_url).exists():
        shortcut = ShortURL.objects.filter(name=custom_url).order_by('-id')[0]
    elif ShortURL.objects.filter(permanent_url=custom_url).exists():
        shortcut = ShortURL.objects.get(permanent_url=custom_url)
    else:
        return redirect('/')

    # create viewer log
    Viewer.objects.create(
        short_url=shortcut,
        ip=request.META.get('REMOTE_ADDR')
    )

    if shortcut.mode == 301:
        return redirect(shortcut.target)
    else:
        image_url = 'https://' + request.get_host()
        image_url += str(shortcut.thumbnail.url) if shortcut.thumbnail else (
            settings.STATIC_URL + '/images/default_thumbnail.png')
        context = {
            'url': shortcut.target,
            'title': shortcut.title,
            'description': shortcut.description,
            'image': image_url
        }
        return render(request, 'links/redirect.html', context)


def perm_url(request, permanent_url):
    if not ShortURL.objects.filter(permanent_url=permanent_url).exists():
        return redirect('/')

    shortcut = ShortURL.objects.get(permanent_url=permanent_url)

    # create viewer log
    Viewer.objects.create(
        short_url=shortcut,
        ip=request.META.get('REMOTE_ADDR')
    )

    if shortcut.mode == 301:
        return redirect(shortcut.target)
    else:
        image_url = 'https://' + request.get_host()
        image_url += str(shortcut.thumbnail.url) if shortcut.thumbnail else (
            settings.STATIC_URL + '/images/default_thumbnail.png')

        context = {
            'url': shortcut.target,
            'title': shortcut.title,
            'description': shortcut.description,
            'image': image_url
        }

        return render(request, 'links/redirect.html', context)


def chart(request, permanent_url):
    shortcut = ShortURL.objects.get(permanent_url=permanent_url)

    last_view = shortcut.viewers.all().order_by('-id')[0].timestamp
    time_pointer = datetime.date(
        year=last_view.year, month=last_view.month, day=last_view.day) - datetime.timedelta(days=10, hours=16)
    labels = list()
    data = list()
    for day in range(10):
        time_pointer += datetime.timedelta(days=1)
        labels.append(time_pointer.strftime("%b %d"))
        data.append(shortcut.viewers.filter(
            timestamp__year=time_pointer.year,
            timestamp__month=time_pointer.month,
            timestamp__day=time_pointer.day,
        ).count())
    context = {
        'BASE_URL': BASE_URL,
        'BASE_SHORT_URL': BASE_SHORT_URL,
        'data': json.dumps(data),
        'labels': json.dumps(labels),
        'permanent_url': shortcut.permanent_url,
        'total_views': shortcut.viewers.all().count(),
        'last_view': shortcut.viewers.all().order_by(
            '-id')[0].timestamp
    }
    return render(request, 'links/chart.html', context)
