from django.urls import path
from . import views

urlpatterns = [
    path('', views.student_list, name='student_list'),
    path('student/<int:student_id>/', views.student_results, name='student_results'),
    path('student/<int:student_id>/fees/', views.student_fees, name='student_fees'),
    path('parent/login/', views.parent_login, name='parent_login'),
    path('parent/dashboard/', views.parent_dashboard, name='parent_dashboard'),
    path('parent/logout/', views.parent_logout, name='parent_logout'),
    path('parent/signup/', views.parent_signup, name='parent_signup'),
    path('teacher/add-mark/', views.add_mark, name='add_mark'),
]