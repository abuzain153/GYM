from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .forms import AddWorkoutForm, WorkoutPlanForm, ExerciseSetFormSet
from .models import Workout, WorkoutDay, ExerciseSet
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.views import LogoutView
@login_required
def delete_workout(request, workout_id):
    workout = get_object_or_404(Workout, id=workout_id, user=request.user)
    if request.method == 'POST':
        workout.delete()
        messages.success(request, "تم حذف التمرين بنجاح.")
        return redirect('home')  # أو توجه لصفحة مناسبة بعد الحذف
    return render(request, 'workout_app/confirm_delete.html', {'workout': workout})

@login_required
def home(request):
    workouts = Workout.objects.filter(user=request.user)
    return render(request, 'workout_app/home.html', {'workouts': workouts})


@login_required
def plan_week_overview(request, week_number=1):
    days_of_week = WorkoutDay.DAYS_OF_WEEK
    context = {
        'week_number': week_number,
        'days_of_week': days_of_week,
        'previous_week': week_number - 1 if week_number > 1 else None,
        'next_week': week_number + 1,
    }
    return render(request, 'workout_app/plan_week_overview.html', context)

@login_required
def view_progress(request):
    exercise_sets = ExerciseSet.objects.filter(workout_day__user=request.user).order_by(
        'workout_day__week_number',
        'workout_day__day_of_week',
        'exercise__name',
        'set_number'
    )

    exercises = Workout.objects.filter(user=request.user).order_by('name').distinct()

    if request.GET.get('exercise'):
        exercise_sets = exercise_sets.filter(exercise_id=request.GET['exercise'])
    if request.GET.get('week'):
        exercise_sets = exercise_sets.filter(workout_day__week_number=request.GET['week'])

    context = {
        'exercise_sets': exercise_sets,
        'exercises': exercises,
    }
    return render(request, 'workout_app/view_progress.html', context)

@login_required
def add_workout(request):
    if request.method == 'POST':
        form = AddWorkoutForm(request.POST)
        if form.is_valid():
            workout = form.save(commit=False)
            workout.user = request.user
            workout.save()
            return redirect('home')
    else:
        form = AddWorkoutForm()
    return render(request, 'workout_app/add_workout.html', {'form': form})

@login_required
def plan_week(request, week_number, day_code):
    day_name = dict(WorkoutDay.DAYS_OF_WEEK).get(day_code, 'غير معروف')
    planned_workouts = WorkoutDay.objects.filter(user=request.user, week_number=week_number, day_of_week=day_code)
    if request.method == 'POST':
        form = WorkoutPlanForm(request.user, week_number, day_code, request.POST)
        if form.is_valid():
            form.save()
            return redirect('plan_day_plan', week_number=week_number, day_code=day_code)
    else:
        form = WorkoutPlanForm(request.user, week_number, day_code)
    return render(request, 'workout_app/plan_week.html', {'form': form, 'week_number': week_number, 'day_name': day_name, 'day_code': day_code, 'planned_workouts': planned_workouts})

@login_required
def edit_week(request, week_number):
    return HttpResponse(f"<h1>صفحة تعديل الأسبوع رقم {week_number}</h1>")

@login_required
def record_set(request, workout_day_id, exercise_id, week_number):
    workout_day = get_object_or_404(WorkoutDay, id=workout_day_id)
    exercise = get_object_or_404(Workout, id=exercise_id)

    if request.method == 'POST':
        formset = ExerciseSetFormSet(request.POST, queryset=ExerciseSet.objects.filter(workout_day=workout_day, exercise=exercise))
        if formset.is_valid():
            instances = formset.save(commit=False)
            for i, instance in enumerate(instances):
                instance.workout_day = workout_day
                instance.exercise = exercise
                instance.set_number = i + 1  # Assign set number automatically
                instance.user = request.user # تأكد إنك بتسند المستخدم هنا لو كان ضروري
                instance.save()
            for obj in formset.deleted_objects:
                obj.delete()
            return redirect('home')  # ممكن نعدل التوجيه لصفحة عرض التقدم بعدين
    else:
        formset = ExerciseSetFormSet(queryset=ExerciseSet.objects.filter(workout_day=workout_day, exercise=exercise))

    return render(request, 'workout_app/record_set.html', {'formset': formset, 'workout_day': workout_day, 'exercise': exercise, 'week_number': week_number})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # قم بتغيير 'home' إلى الرابط الذي تريد إعادة التوجيه إليه بعد تسجيل الدخول
    else:
        form = AuthenticationForm()
    # قم بتغيير اسم القالب هنا ليشير إلى المسار الذي ذكرته
    return render(request, 'registration/login.html', {'form': form})
