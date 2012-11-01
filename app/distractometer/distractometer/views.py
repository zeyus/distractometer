from django.shortcuts import render_to_response
from django.template import RequestContext
import datetime
from .models import Distraction, Person, Settings
from django.db.models import Sum
import json
from django.core.exceptions import ObjectDoesNotExist

def index(request):

    distractions = list(Distraction.objects.values('person').filter(time__gte=datetime.date.today()).annotate(duration=Sum('duration')))
#    distraction_day = json.dumps(distractions)
    distraction_day_data = [
        ['Range'],
        ['Today']
    ]
    distraction_day_colors = []

    for d in distractions:
        p = Person.objects.get(pk=d['person'])
        distraction_day_data[0].append(p.name)
        distraction_day_data[1].append(d['duration'])
        distraction_day_colors.append({'color':'#'+p.color})

    distraction_day_data = json.dumps(distraction_day_data)
    distraction_day_colors = json.dumps(distraction_day_colors)

    try:
        staff_count=int(Settings.objects.get(name='staff_count').value)
    except ObjectDoesNotExist:
        staff_count=1

    try:
        work_day_hours=int(Settings.objects.get(name='work_day_hours').value)
    except ObjectDoesNotExist:
        work_day_hours=8


    max_seconds = staff_count*60*60*work_day_hours

    return render_to_response('index.html', RequestContext(request,{'week':'asdf','day':distraction_day_data,'day_colors':distraction_day_colors,'max_seconds':max_seconds}))

