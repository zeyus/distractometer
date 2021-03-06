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

    time = models.DateTimeField(default=datetime.datetime.now())
    duration = models.IntegerField(default=60)
    person = models.ForeignKey(Person)
    description = models.TextField(blank=True)
    def __unicode__(self):
        return self.person.name + ' ' + str(self.duration )
    @staticmethod
    def getChartDistractions(date=None):

        if date is None:
            date = datetime.date.today()

        distractions = list(Distraction.objects.values('person','duration').filter(time__gte=date).order_by('time'))
        distraction_day_data = {
            'cols':[{'id':'Range','label':'Duration', 'type':'string'}, {'id':'emptyentry','label':'','type':'number'}],
            'rows':[{'c':[{'v':'Today'}, {'v':0}]}]
            }
        distraction_day_colors = [{'color':'#000000'},]
        total = 0
        multiplier = int(Settings.getSetting('distraction_multiplier',1))
        for d in distractions:
            duration = multiplier*d['duration']
            p = Person.objects.get(pk=d['person'])
            distraction_day_data['cols'].append({'id':p.name,'label':p.name,'type':'number'})
            distraction_day_data['rows'][0]['c'].append({'v':duration,'f':str(datetime.timedelta(seconds=d['duration']))})
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
        else:
            monday = date - datetime.timedelta(days=date.weekday())
            friday = monday + datetime.timedelta(days=5)
        distractions = Distraction.objects.filter(time__gte=monday, time__lte=friday).extra(
            select = {"date": """DATE(time)"""}).values('date').annotate(duration=Sum('duration'))

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
            max_seconds = Settings.getMaxDistractions()
            a,b = linreg(range(len(trend_vals)),trend_vals)

            for k,day in enumerate(per_day_list):
                per_day_list[k]['trendline'] = min(max(a*k+b,0),max_seconds)
                if today.weekday() > k:
                    per_day_list[k]['certainty'] = True
                else:
                    per_day_list[k]['certainty'] = False
        else:
            for k,day in enumerate(per_day_list):
                per_day_list[k]['trendline'] = 0
                per_day_list[k]['certainty'] = False


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
