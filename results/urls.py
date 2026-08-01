from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about_us, name='about_us'),
    path('services/', views.our_services, name='our_services'),

    path('student/<int:student_id>/', views.student_results, name='student_results'),
    path('student/<int:student_id>/fees/', views.student_fees, name='student_fees'),
    path('student/<int:student_id>/report-card/', views.download_report_card, name='download_report_card'),
    path('student/<int:student_id>/fee-statement/', views.download_fee_statement, name='download_fee_statement'),

    path('parent/login/', views.parent_login, name='parent_login'),
    path('parent/dashboard/', views.parent_dashboard, name='parent_dashboard'),
    path('parent/logout/', views.parent_logout, name='parent_logout'),
    path('parent/signup/', views.parent_signup, name='parent_signup'),
    path('parent/forgot-password/', views.parent_forgot_password, name='parent_forgot_password'),

    path('school/signup/', views.school_signup, name='school_signup'),
    path('school/login/', views.school_login, name='school_login'),
    path('school/dashboard/', views.school_dashboard, name='school_dashboard'),
    path('school/forgot-password/', views.school_forgot_password, name='school_forgot_password'),
    path('school/delete/', views.delete_school_account, name='delete_school_account'),
    path('school/<int:school_id>/teacher/signup/', views.teacher_signup, name='teacher_signup'),
    path('school/<int:school_id>/accountant/signup/', views.accountant_signup, name='accountant_signup'),

    path('teacher/login/', views.teacher_login, name='teacher_login'),
    path('teacher/dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('teacher/logout/', views.teacher_logout, name='teacher_logout'),
    path('teacher/add-student/', views.teacher_add_student, name='teacher_add_student'),
    path('teacher/add-mark/', views.add_mark, name='add_mark'),
    path('teacher/forgot-password/', views.teacher_forgot_password, name='teacher_forgot_password'),
    path('teacher/delete/', views.delete_teacher_account, name='delete_teacher_account'),
    path('teacher/signup/select/', views.teacher_signup_select_school, name='teacher_signup_select'),
    path('teacher/student/<int:student_id>/edit/', views.teacher_edit_student, name='teacher_edit_student'),
    path('teacher/student/<int:student_id>/delete/', views.teacher_delete_student, name='teacher_delete_student'),

    path('accountant/login/', views.accountant_login, name='accountant_login'),
    path('accountant/dashboard/', views.accountant_dashboard, name='accountant_dashboard'),
    path('accountant/logout/', views.accountant_logout, name='accountant_logout'),
    path('accountant/add-fee-structure/', views.add_fee_structure, name='add_fee_structure'),
    path('accountant/record-payment/', views.record_payment, name='record_payment'),
    path('accountant/forgot-password/', views.accountant_forgot_password, name='accountant_forgot_password'),
    path('accountant/delete/', views.delete_accountant_account, name='delete_accountant_account'),
    path('accountant/signup/select/', views.accountant_signup_select_school, name='accountant_signup_select'),
    path('accountant/fee/<int:fee_id>/edit/', views.accountant_edit_fee_structure, name='accountant_edit_fee'),
    path('accountant/fee/<int:fee_id>/delete/', views.accountant_delete_fee_structure, name='accountant_delete_fee'),
    path('accountant/payment/<int:payment_id>/edit/', views.accountant_edit_payment, name='accountant_edit_payment'),
    path('accountant/payment/<int:payment_id>/delete/', views.accountant_delete_payment, name='accountant_delete_payment'),
]