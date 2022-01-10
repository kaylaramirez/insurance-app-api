from django.contrib import admin

from quote import models

admin.site.register(models.Quote)
admin.site.register(models.Address)
