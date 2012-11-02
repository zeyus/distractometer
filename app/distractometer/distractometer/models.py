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
        for d in distractions:
            p = Person.objects.get(pk=d['person'])
            distraction_day_data[0].append(p.name)
            distraction_day_data[1].append(d['duration'])
            total += d['duration']
            distraction_day_colors.append({'color':'#'+p.color})

        distraction_day_data = json.dumps(distraction_day_data)
        distraction_day_colors = json.dumps(distraction_day_colors)

        return {'data':distraction_day_data,'colors':distraction_day_colors,'total':total }




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