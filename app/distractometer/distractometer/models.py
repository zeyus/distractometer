import datetime, json
from django.db.models import Sum
from django.db import models

class Person(models.Model):
    name = models.CharField(max_length=50)
    distractoids = models.IntegerField()
    color = models.CharField(max_length=6)
    def __unicode__(self):
        return self.name

class Distraction(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    duration = models.IntegerField()
    person = models.ForeignKey(Person)
    description = models.TextField(blank=True)
    def __unicode__(self):
        return self.person.name + ' ' + str(self.duration )
    @staticmethod
    def getChartDistractions(date=None):

        if date is None:
            date = datetime.date.today()

        #distractions = list(Distraction.objects.values('person').filter(time__gte=date).annotate(duration=Sum('duration')))
        distractions = list(Distraction.objects.values('person','duration').filter(time__gte=date).order_by('time'))
        distraction_day_data = [
            ['Range'],
            ['Today']
        ]
        distraction_day_colors = []
        total = 0
        multiplier = int(Settings.getSetting('distraction_multiplier',1))
        for d in distractions:
            duration = multiplier*d['duration']
            p = Person.objects.get(pk=d['person'])
            distraction_day_data[0].append(p.name)
            distraction_day_data[1].append(duration)
            total += duration
            distraction_day_colors.append({'color':'#'+p.color})

        distraction_day_data = json.dumps(distraction_day_data)
        distraction_day_colors = json.dumps(distraction_day_colors)

        return {'data':distraction_day_data,'colors':distraction_day_colors,'total':total }

    @staticmethod
    def getChartDistractionsWeek(date=None):
        trend_end = 5

        if date is None:
            today = datetime.date.today()
            if today.weekday() < 5:
                trend_end = today.weekday()

            monday = today - datetime.timedelta(days=today.weekday())
            friday = monday + datetime.timedelta(days=5)
            #date = datetime.date.today()
        else:
            monday = date - datetime.timedelta(days=date.weekday())
            friday = monday + datetime.timedelta(days=5)
        distractions = Distraction.objects.filter(time__gte=monday, time__lte=friday).extra(
            select = {"date": """DATE(time)"""}).values('date').annotate(duration=Sum('duration'))

        #distractions_week = []
        #for d in distractions:
        #    distractions_week.append({'date': d['date'],'duration': d['duration']})

        per_day = {}
        multiplier = int(Settings.getSetting('distraction_multiplier',1))
        for d in distractions:
            per_day[str(d['date'])] = d['duration']*multiplier

        d = 0
        per_day_list = []
        trend_vals = []
        while d < 5:
            day = monday + datetime.timedelta(days=d)
            day=str(day)
            if not per_day.has_key(day):
                per_day[day] = 0

            trend_vals.append(int(per_day[day]))
            per_day_list.append({'date':day,'duration':per_day[day]})
            d += 1


        if trend_end > 0:
            trend_vals = trend_vals[0:trend_end]

            a,b = linreg(range(len(trend_vals)),trend_vals)
            #if trend_end < 4:
            #    trend_line=[a*index + b for index in range(5)]
            for k,day in enumerate(per_day_list):
                per_day_list[k]['trendline'] = max(a*(k+1)+b,0)
        else:
            for k,day in enumerate(per_day_list):
                per_day_list[k]['trendline'] = 0


        return per_day_list




class Category(models.Model):
    name = models.CharField(max_length=50)
    parent = models.ForeignKey('self', blank=True, null=True)
    def __unicode__(self):
        return self.name

class Item(models.Model):
    name = models.CharField(max_length=50)
    price = models.IntegerField()
    description = models.TextField()
    category = models.ForeignKey(Category)
    def __unicode__(self):
        return self.name

class Transaction(models.Model):
    person = models.ForeignKey(Person)
    time = models.DateTimeField(auto_now_add=True)
    item = models.ForeignKey(Item)
    amount = models.IntegerField()
    def __unicode__(self):
        return str(self.time) + ' ' + self.person.name

class Settings(models.Model):
    name = models.CharField(max_length=50,unique=True)
    value = models.TextField()
    def __unicode__(self):
        return self.name
    @staticmethod
    def getSetting(key,default=None):
        try:
            val=Settings.objects.get(name=key).value
        except Settings.DoesNotExist:
            val=default

        return val

    @staticmethod
    def getMaxDistractions():
        return int(Settings.getSetting('staff_count',1))*60*60*int(Settings.getSetting('work_day_hours',8))


def linreg(X, Y):
    """
    return a,b in solution to y = ax + b such that root mean square distance between trend line and original points is minimized
    """
    N = len(X)
    Sx = Sy = Sxx = Syy = Sxy = 0.0
    for x, y in zip(X, Y):
        Sx = Sx + x
        Sy = Sy + y
        Sxx = Sxx + x*x
        Syy = Syy + y*y
        Sxy = Sxy + x*y
    det = Sxx * N - Sx * Sx
    if det == 0:
        return Sxy * N - Sy * Sx, Sxx * Sy - Sx * Sxy
    return (Sxy * N - Sy * Sx)/det, (Sxx * Sy - Sx * Sxy)/det
