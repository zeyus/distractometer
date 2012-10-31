from django.shortcuts import render_to_response
from django.template import RequestContext
from .models import Distraction as Distraction
from .models import Person as Person
from django.db.models import Sum
import json 

def index(request):

    distractions = list(Distraction.objects.values('person').annotate(duration=Sum('duration')))
#    distraction_day = json.dumps(distractions)
    distraction_day = []
    for d in distractions:
        distraction_day.append({
            'duration': d['duration'],
            'person': Person.objects.get(pk=d['person']).name,
        })


    return render_to_response('index.html', RequestContext(request,{'week':'asdf','day':distraction_day}))

