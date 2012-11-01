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
