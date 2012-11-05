from django.shortcuts import render_to_response
from django.template import RequestContext
from .models import Settings, Distraction
import datetime,json

def index(request):

    distractions = Distraction.getChartDistractions()
    max_seconds = int(Settings.getSetting('staff_count',1))*60*60*int(Settings.getSetting('work_day_hours',8))

    gauge = round(100 * float(distractions['total'])*int(Settings.getSetting('distraction_multiplier',1))/float(max_seconds), ndigits=1)

    distractions_week = Distraction.getChartDistractionsWeek()

    week = []
    for day in distractions_week:
        week.append([day['date'],day['duration'],day['trendline']])

    distractions_week = json.dumps(week)


    return render_to_response('index.html', RequestContext(request,{'week':distractions_week,'day':distractions['data'],'day_colors':distractions['colors'],'gauge':gauge}))

