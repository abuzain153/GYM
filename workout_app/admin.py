from django.contrib import admin
from .models import Workout, WorkoutDay, ExerciseSet

# Register your models here.
admin.site.register(Workout)
admin.site.register(WorkoutDay)
admin.site.register(ExerciseSet)
