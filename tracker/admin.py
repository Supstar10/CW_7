from django.contrib import admin
from .models import Habit


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ('action', 'user', 'time', 'pleasant_habit', 'is_public')
    list_filter = ('pleasant_habit', 'is_public')
    search_fields = ('action', 'user__username')
