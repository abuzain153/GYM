from django.db import models
from django.contrib.auth.models import User

class Workout(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class WorkoutDay(models.Model):
    DAYS_OF_WEEK = [
        ('Sat', 'السبت'),
        ('Sun', 'الأحد'),
        ('Mon', 'الاثنين'),
        ('Tue', 'الثلاثاء'),
        ('Wed', 'الأربعاء'),
        ('Thu', 'الخميس'),
    ]
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # إضافة حقل المستخدم هنا
    day_of_week = models.CharField(max_length=3, choices=DAYS_OF_WEEK)
    week_number = models.IntegerField(default=1) # إضافة قيمة افتراضية للأسبوع

    class Meta:
        unique_together = ('workout', 'user', 'day_of_week', 'week_number') # تضمين المستخدم في القيود الفريدة

    def __str__(self):
        return f"{self.workout.name} - أسبوع {self.week_number} - {self.get_day_of_week_display()}"

class ExerciseSet(models.Model):
    workout_day = models.ForeignKey(WorkoutDay, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Workout, on_delete=models.CASCADE)
    set_number = models.IntegerField()
    repetitions = models.IntegerField()
    weight = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        unique_together = ('workout_day', 'exercise', 'set_number')
        ordering = ['set_number']

    def __str__(self):
        return f"جولة {self.set_number} - {self.exercise.name} ({self.repetitions} عدة بوزن {self.weight})"
