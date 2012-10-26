from django.shortcuts import render_to_response
from django.template import RequestContext
from .models import Distraction as Distraction
from django.db.models import Sum
import json 

def index(request):

    distractions = Distraction.objects.values('person').annotate(Sum('duration'))
    #distractions_day = json.dumps(distractions)
    distraction_day = [{
        #'time': d.time,
        'duration': d.get('duration__sum'),
        'person': d.get('person'),
    } for d in distractions]

    return render_to_response('index.html', RequestContext(request,{'week':'asdf','day':distraction_day}))

