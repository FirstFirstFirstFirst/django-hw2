from django.contrib import admin

from .models import *

# Register your models here.

admin.site.register(Product)
admin.site.register(ContactList)
admin.site.register(Profile)
admin.site.register(Action)
admin.site.register(Prompt)
admin.site.register(TestCase)
admin.site.register(Result)