# workout_app/forms.py
from django import forms
from .models import Workout, WorkoutDay
from .models import ExerciseSet

class AddWorkoutForm(forms.ModelForm):
    day_of_week = forms.ChoiceField(
        choices=WorkoutDay.DAYS_OF_WEEK,
        label='اليوم'
    )

    class Meta:
        model = Workout
        fields = ['name']
        labels = {
            'name': 'اسم التمرين',
        }

class WorkoutPlanForm(forms.Form):
    def __init__(self, user, week_number, day_code, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self.week_number = week_number
        self.day_code = day_code
        workouts = Workout.objects.filter(user=user)
        planned_workouts = WorkoutDay.objects.filter(
            workout__user=user,
            week_number=week_number,
            day_of_week=day_code
        ).values_list('workout_id', flat=True)

        self.fields['workouts'] = forms.ModelMultipleChoiceField(
            queryset=workouts,
            widget=forms.CheckboxSelectMultiple,
            label='تمارين هذا اليوم',
            initial=list(planned_workouts),
            required=False
        )

    def save(self):
        selected_workouts = self.cleaned_data.get('workouts')
        if selected_workouts:
            WorkoutDay.objects.filter(
                workout__user=self.user,
                day_of_week=self.day_code,
                week_number=self.week_number
            ).delete()  # Remove existing plan
            for workout in selected_workouts:
                WorkoutDay.objects.create(
                    workout=workout,
                    day_of_week=self.day_code,
                    week_number=self.week_number,
                    user=self.user  # تعيين المستخدم الحالي هنا!
                )


class ExerciseSetForm(forms.ModelForm):
    class Meta:
        model = ExerciseSet
        fields = ['repetitions', 'weight']  # تم إزالة 'set_number' من هنا
        labels = {
            'repetitions': 'العدات',
            'weight': 'الوزن (كجم)',
        }
        widgets = {
            'repetitions': forms.NumberInput(attrs={'class': 'form-control'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control'}),
        }

ExerciseSetFormSet = forms.modelformset_factory(
    ExerciseSet,
    form=ExerciseSetForm,
    extra=3,  # عدد الجولات الافتراضي اللي هيظهر
    can_delete=True
)
