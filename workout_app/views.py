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
    print(f"delete_workout: Starting for workout_id={workout_id}")  # Debugging
    workout = get_object_or_404(Workout, id=workout_id, user=request.user)
    if request.method == 'POST':
        workout.delete()
        messages.success(request, "تم حذف التمرين بنجاح.")
        print("delete_workout: Workout deleted successfully")  # Debugging
        return redirect('home')
    print("delete_workout: Returning confirmation page")  # Debugging
    return render(request, 'workout_app/confirm_delete.html', {'workout': workout})

@login_required
def home(request):
    print("home: Starting")  # Debugging
    workouts = Workout.objects.filter(user=request.user)
    print(f"home: Found {workouts.count()} workouts")  # Debugging
    return render(request, 'workout_app/home.html', {'workouts': workouts})

@login_required
def plan_week_overview(request, week_number=1):
    print(f"plan_week_overview: Starting for week_number={week_number}")  # Debugging
    days_of_week = WorkoutDay.DAYS_OF_WEEK
    context = {
        'week_number': week_number,
        'days_of_week': days_of_week,
        'previous_week': week_number - 1 if week_number > 1 else None,
        'next_week': week_number + 1,
    }
    print("plan_week_overview: Returning overview page")  # Debugging
    return render(request, 'workout_app/plan_week_overview.html', context)

@login_required
def view_progress(request):
    print("view_progress: Starting")  # Debugging
    exercise_sets = ExerciseSet.objects.filter(workout_day__user=request.user).order_by(
        'workout_day__week_number',
        'workout_day__day_of_week',
        'exercise__name',
        'set_number'
    )
    exercises = Workout.objects.filter(user=request.user).order_by('name').distinct()

    if request.GET.get('exercise'):
        exercise_sets = exercise_sets.filter(exercise_id=request.GET['exercise'])
        print(f"view_progress: Filtered by exercise={request.GET['exercise']}")  # Debugging
    if request.GET.get('week'):
        exercise_sets = exercise_sets.filter(workout_day__week_number=request.GET['week'])
        print(f"view_progress: Filtered by week={request.GET['week']}")  # Debugging

    context = {
        'exercise_sets': exercise_sets,
        'exercises': exercises,
    }
    print("view_progress: Returning progress page")  # Debugging
    return render(request, 'workout_app/view_progress.html', context)

@login_required
def add_workout(request):
    print("add_workout: Starting")  # Debugging
    if request.method == 'POST':
        form = AddWorkoutForm(request.POST)
        if form.is_valid():
            workout = form.save(commit=False)
            workout.user = request.user
            workout.save()
            print("add_workout: Workout added successfully")  # Debugging
            return redirect('home')
        else:
            print("add_workout: Form is invalid")  # Debugging
            print(form.errors)  # Debugging - Print form errors
    else:
        form = AddWorkoutForm()
    print("add_workout: Returning form page")  # Debugging
    return render(request, 'workout_app/add_workout.html', {'form': form})

@login_required
def plan_week(request, week_number, day_code):
    print(f"plan_week: Starting for week_number={week_number}, day_code={day_code}")  # Debugging
    day_name = dict(WorkoutDay.DAYS_OF_WEEK).get(day_code, 'غير معروف')
    planned_workouts = WorkoutDay.objects.filter(user=request.user, week_number=week_number, day_of_week=day_code)
    if request.method == 'POST':
        form = WorkoutPlanForm(request.user, week_number, day_code, request.POST)
        if form.is_valid():
            form.save()
            print("plan_week: Plan saved successfully")  # Debugging
            return redirect('plan_day_plan', week_number=week_number, day_code=day_code)
        else:
            print("plan_week: Form is invalid")  # Debugging
            print(form.errors)  # Debugging - Print form errors
    else:
        form = WorkoutPlanForm(request.user, week_number, day_code)
    print("plan_week: Returning form page")  # Debugging
    return render(request, 'workout_app/plan_week.html', {'form': form, 'week_number': week_number, 'day_name': day_name, 'day_code': day_code, 'planned_workouts': planned_workouts})

@login_required
def edit_week(request, week_number):
    print(f"edit_week: Starting for week_number={week_number}")  # Debugging
    # This view currently returns a simple HttpResponse. If it's causing issues,
    # consider what data it's trying to access and if that's causing an error.
    return HttpResponse(f"<h1>صفحة تعديل الأسبوع رقم {week_number}</h1>")

@login_required
def record_set(request, workout_day_id, exercise_id, week_number):
    print(f"record_set: Starting for workout_day_id={workout_day_id}, exercise_id={exercise_id}, week_number={week_number}")  # Debugging
    workout_day = get_object_or_404(WorkoutDay, id=workout_day_id)
    exercise = get_object_or_404(Workout, id=exercise_id)

    if request.method == 'POST':
        formset = ExerciseSetFormSet(request.POST, queryset=ExerciseSet.objects.filter(workout_day=workout_day, exercise=exercise))
        if formset.is_valid():
            instances = formset.save(commit=False)
            for i, instance in enumerate(instances):
                instance.workout_day = workout_day
                instance.exercise = exercise
                instance.set_number = i + 1
                instance.user = request.user  # تأكد إنك بتسند المستخدم هنا لو كان ضروري
                instance.save()
            for obj in formset.deleted_objects:
                obj.delete()
            print("record_set: Sets recorded successfully")  # Debugging
            return redirect('home')  # ممكن نعدل التوجيه لصفحة عرض التقدم بعدين
        else:
            print("record_set: Formset is invalid")  # Debugging
            print(formset.errors)  # Debugging - Print formset errors
    else:
        formset = ExerciseSetFormSet(queryset=ExerciseSet.objects.filter(workout_day=workout_day, exercise=exercise))

    print("record_set: Returning form page")  # Debugging
    return render(request, 'workout_app/record_set.html', {'formset': formset, 'workout_day': workout_day, 'exercise': exercise, 'week_number': week_number})

def login_view(request):
    print("login_view: Starting")  # Debugging
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user is not None:
                login(request, user)
                print("login_view: Login successful")  # Debugging
                return redirect('home')
            else:
                print("login_view: Authentication failed")  # Debugging
                return render(request, 'registration/login.html', {'form': form, 'error_message': 'Invalid credentials'})
        else:
            print("login_view: Form is invalid")  # Debugging
            print(form.errors)  # Debugging - Print form errors
    else:
        form = AuthenticationForm()
    print("login_view: Returning login page")  # Debugging
    return render(request, 'registration/login.html', {'form': form})
