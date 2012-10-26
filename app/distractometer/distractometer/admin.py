from django.contrib import admin
from .models import Person, Distraction, Category, Transaction, Item

admin.site.register(Person)
admin.site.register(Distraction)
admin.site.register(Category)
admin.site.register(Transaction)
admin.site.register(Item)

