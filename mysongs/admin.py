from django.contrib import admin
from .models import Albumtable, Ratingtable, Songstable

admin.site.register(Albumtable)
admin.site.register(Songstable)
admin.site.register(Ratingtable)

