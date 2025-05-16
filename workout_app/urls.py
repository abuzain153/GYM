from django.urls import path
from . import views
# لا يوجد هنا أي تعريف لمسار 'logout'

urlpatterns = [
    path('', views.home, name='home'),
    path('add_workout/', views.add_workout, name='add_workout'),
    path('plan_week/<int:week_number>/<str:day_code>/', views.plan_week, name='plan_day_plan'),
    path('plan_week_overview/', views.plan_week_overview, name='plan_week_overview'),
    path('plan_week_overview/<int:week_number>/', views.plan_week_overview, name='plan_week_overview_with_number'),
    path('record_set/<int:workout_day_id>/<int:exercise_id>/<int:week_number>/', views.record_set, name='record_set'),
    path('progress/', views.view_progress, name='view_progress'),
    path('edit_week/<int:week_number>/', views.edit_week, name='edit_week'),
    path('login/', views.login_view, name='login'),
    path('workout/delete/<int:workout_id>/', views.delete_workout, name='delete_workout'),
    # ... باقي مسارات تطبيق workout_app ...
]
