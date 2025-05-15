from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # الصفحة الرئيسية
    path('add_workout/', views.add_workout, name='add_workout'),
    path('plan_week/<int:week_number>/<str:day_code>/', views.plan_week, name='plan_day_plan'),
    path('plan_week_overview/', views.plan_week_overview, name='plan_week_overview'),
    path('plan_week_overview/<int:week_number>/', views.plan_week_overview, name='plan_week_overview_with_number'),
    path('record_set/<int:workout_day_id>/<int:exercise_id>/<int:week_number>/', views.record_set, name='record_set'),
    path('progress/', views.view_progress, name='view_progress'),  # URL جديد لعرض التقدم
    path('edit_week/<int:week_number>/', views.edit_week, name='edit_week'),
    path('login/', views.login_view, name='login'),  # إضافة مسار تسجيل الدخول هنا
    # ممكن نضيف هنا URLs تانية زي تعديل الجولات، عرض التقدم بشكل مفصل لتمرين معين، إلخ.
]
