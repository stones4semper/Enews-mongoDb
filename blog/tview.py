import json
from django.shortcuts import *
from django.template import RequestContext
from linki.forms import *

def advert(request):
    if request.method == "POST":
        form = AdvertForm(request.POST)

        message = 'something wrong!'
        if(form.is_valid()):
            print(request.POST['title'])
            message = request.POST['title']

        return HttpResponse(json.dumps({'message': message}))

    return render_to_response('contact/advert.html',
            {'form':AdvertForm()}, RequestContext(request))