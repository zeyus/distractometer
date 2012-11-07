from django.shortcuts import render_to_response
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.template import RequestContext
from .models import Settings, Distraction
from .forms import DistractionForm
import datetime,json

def index(request):
    show_add = request.user.has_perm('distractometer.add_distraction')
    form = None
    if show_add:
        if request.method == 'POST' and 'add_distraction' in request.POST:
            form = DistractionForm(prefix='distraction',data=request.POST)
            if form.is_valid():
                form.save()
        else:
            form = DistractionForm(prefix='distraction')

    distractions = Distraction.getChartDistractions()

    max_seconds = Settings.getMaxDistractions()

    gauge = round(100 * float(distractions['total'])/float(max_seconds), ndigits=1)

    distractions_week = Distraction.getChartDistractionsWeek()

    week = []
    for day in distractions_week:
        week.append([day['date'],day['duration'],day['trendline'],day['certainty']])

    distractions_week = json.dumps(week)


    return render_to_response('index.html', RequestContext(request,{'week':distractions_week,'day':distractions['data'],'day_colors':distractions['colors'],'gauge':gauge,'max':max_seconds,'distraction_form':form, 'show_add':show_add}))


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')

def add_distraction(request):



    return HttpResponseRedirect('/')
