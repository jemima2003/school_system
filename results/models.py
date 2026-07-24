from django.db import models


class School(models.Model):
    LEVEL_CHOICES = [
        ('primary', 'Primary School'),
        ('secondary', 'Secondary School'),
    ]
    name = models.CharField(max_length=100)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default='primary')
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Teacher(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    password = models.CharField(max_length=100)
    grade = models.IntegerField()

    def __str__(self):
        return f"{self.full_name} (Grade {self.grade})"


class Accountant(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.full_name


class Student(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    added_by = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True)
    full_name = models.CharField(max_length=100)
    admission_number = models.CharField(max_length=20)
    grade = models.IntegerField()
    stream = models.CharField(max_length=20, blank=True)
    verification_code = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return self.full_name


class Subject(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    grade = models.IntegerField()

    def __str__(self):
        return self.name


class Assessment(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    term = models.IntegerField()
    academic_year = models.IntegerField()

    def __str__(self):
        return f"{self.name} - Term {self.term} ({self.academic_year})"


class Mark(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE)
    score = models.FloatField()
    max_score = models.FloatField(default=100)

    def __str__(self):
        return f"{self.student} - {self.subject} - {self.assessment}: {self.score}"


class FeeStructure(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    grade = models.IntegerField()
    term = models.IntegerField()
    academic_year = models.IntegerField()
    amount_due = models.FloatField()

    def __str__(self):
        return f"Grade {self.grade} - Term {self.term} ({self.academic_year}): {self.amount_due}"


class Payment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    recorded_by = models.ForeignKey(Accountant, on_delete=models.SET_NULL, null=True, blank=True)
    amount_paid = models.FloatField()
    date_paid = models.DateField()
    payment_method = models.CharField(max_length=30, blank=True)
    reference_number = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"{self.student} - {self.amount_paid} on {self.date_paid}"


class Parent(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.CharField(max_length=100, blank=True)
    password = models.CharField(max_length=100)
    students = models.ManyToManyField(Student)

    def __str__(self):
        return self.full_name