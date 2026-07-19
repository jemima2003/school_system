from django.contrib import admin
from .models import Student, Subject, Assessment, Mark, FeeStructure, Payment, Parent, School, Teacher

admin.site.register(Student)
admin.site.register(Subject)
admin.site.register(Assessment)
admin.site.register(Mark)
admin.site.register(FeeStructure)
admin.site.register(Payment)
admin.site.register(Parent)
admin.site.register(School)
admin.site.register(Teacher)