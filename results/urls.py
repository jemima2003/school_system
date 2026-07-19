from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('student/<int:student_id>/', views.student_results, name='student_results'),
    path('student/<int:student_id>/fees/', views.student_fees, name='student_fees'),
    path('student/<int:student_id>/report-card/', views.download_report_card, name='download_report_card'),
    path('student/<int:student_id>/fee-statement/', views.download_fee_statement, name='download_fee_statement'),
    path('parent/login/', views.parent_login, name='parent_login'),
    path('parent/dashboard/', views.parent_dashboard, name='parent_dashboard'),
    path('parent/logout/', views.parent_logout, name='parent_logout'),
    path('parent/signup/', views.parent_signup, name='parent_signup'),
    path('teacher/add-mark/', views.add_mark, name='add_mark'),
    path('school/signup/', views.school_signup, name='school_signup'),
    path('school/login/', views.school_login, name='school_login'),
    path('school/dashboard/', views.school_dashboard, name='school_dashboard'),
    path('school/<int:school_id>/teacher/signup/', views.teacher_signup, name='teacher_signup'),
    path('teacher/login/', views.teacher_login, name='teacher_login'),
    path('teacher/dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('teacher/logout/', views.teacher_logout, name='teacher_logout'),
    path('teacher/add-student/', views.teacher_add_student, name='teacher_add_student'),
    path('school/<int:school_id>/accountant/signup/', views.accountant_signup, name='accountant_signup'),
    path('accountant/login/', views.accountant_login, name='accountant_login'),
    path('accountant/dashboard/', views.accountant_dashboard, name='accountant_dashboard'),
    path('accountant/logout/', views.accountant_logout, name='accountant_logout'),
    path('accountant/add-fee-structure/', views.add_fee_structure, name='add_fee_structure'),
    path('accountant/record-payment/', views.record_payment, name='record_payment'),
]