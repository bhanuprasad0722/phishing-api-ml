from django.contrib import admin
from .models import Predictions


@admin.register(Predictions)
class PredictionAdmin(admin.ModelAdmin):
    list_display = ('user','prediction','confidence','created_at')
    list_filter = ('prediction','created_at')
    search_fields = ('url','user__username')

# Register your models here.
