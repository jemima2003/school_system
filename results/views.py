from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from .models import Student, Mark, FeeStructure, Payment, Parent, School, Teacher, Subject, Assessment, Accountant
from .forms import MarkForm, ParentSignupForm, SchoolSignupForm, TeacherSignupForm, AccountantSignupForm
from .forms import MarkForm, ParentSignupForm, SchoolSignupForm, TeacherSignupForm, AccountantSignupForm, ForgotPasswordForm


def home(request):
    return render(request, 'results/home.html')


def get_grade(percentage):
    if percentage >= 80:
        return "A"
    elif percentage >= 70:
        return "B"
    elif percentage >= 60:
        return "C"
    elif percentage >= 50:
        return "D"
    else:
        return "E"


def can_access_student(request, student):
    parent_id = request.session.get('parent_id')
    if parent_id:
        return Parent.objects.filter(id=parent_id, students=student).exists()

    teacher_id = request.session.get('teacher_id')
    if teacher_id:
        return Teacher.objects.filter(id=teacher_id, school=student.school).exists()

    accountant_id = request.session.get('accountant_id')
    if accountant_id:
        return Accountant.objects.filter(id=accountant_id, school=student.school).exists()

    school_id = request.session.get('school_id')
    if school_id:
        return student.school_id == school_id

    return False


def student_results(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if not can_access_student(request, student):
        return redirect('home')

    marks = Mark.objects.filter(student=student)

    total = sum(m.score for m in marks)
    max_total = sum(m.max_score for m in marks)
    average = total / len(marks) if marks else 0
    percentage = (total / max_total * 100) if max_total else 0
    grade = get_grade(percentage)

    context = {
        'student': student,
        'marks': marks,
        'total': total,
        'average': average,
        'percentage': percentage,
        'grade': grade,
    }
    return render(request, 'results/student_results.html', context)


def student_fees(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if not can_access_student(request, student):
        return redirect('home')

    fee_structure = FeeStructure.objects.filter(school=student.school, grade=student.grade).first()
    amount_due = fee_structure.amount_due if fee_structure else 0

    payments = Payment.objects.filter(student=student)
    total_paid = sum(p.amount_paid for p in payments)

    balance = amount_due - total_paid

    context = {
        'student': student,
        'amount_due': amount_due,
        'payments': payments,
        'total_paid': total_paid,
        'balance': balance,
    }
    return render(request, 'results/student_fees.html', context)


def parent_login(request):
    error = None
    schools = School.objects.all()
    if request.method == 'POST':
        school_id = request.POST.get('school')
        phone = request.POST.get('phone')
        password = request.POST.get('password')

        parent = Parent.objects.filter(school_id=school_id, phone=phone).first()

        if parent and check_password(password, parent.password):
            request.session['parent_id'] = parent.id
            return redirect('parent_dashboard')
        else:
            error = "Invalid school, phone, or password"

    return render(request, 'results/parent_login.html', {'error': error, 'schools': schools})


def parent_dashboard(request):
    parent_id = request.session.get('parent_id')
    if not parent_id:
        return redirect('parent_login')

    parent = get_object_or_404(Parent, id=parent_id)
    students = parent.students.all()

    return render(request, 'results/parent_dashboard.html', {'parent': parent, 'students': students})


def parent_logout(request):
    request.session.flush()
    return redirect('parent_login')


def parent_signup(request):
    error = None
    if request.method == 'POST':
        form = ParentSignupForm(request.POST)
        if form.is_valid():
            school = form.cleaned_data['school']
            admission_number = form.cleaned_data['admission_number']
            verification_code = form.cleaned_data['verification_code']

            student = Student.objects.filter(
                school=school,
                admission_number=admission_number,
                verification_code=verification_code
            ).first()

            if student:
                parent = Parent.objects.create(
                    school=school,
                    full_name=form.cleaned_data['full_name'],
                    phone=form.cleaned_data['phone'],
                    email=form.cleaned_data['email'],
                    password=make_password(form.cleaned_data['password']),
                )
                parent.students.add(student)
                return redirect('parent_login')
            else:
                error = "Admission number or verification code is incorrect for the selected school"
    else:
        form = ParentSignupForm()

    return render(request, 'results/parent_signup.html', {'form': form, 'error': error})


def school_signup(request):
    error = None
    if request.method == 'POST':
        form = SchoolSignupForm(request.POST)
        if form.is_valid():
            School.objects.create(
                name=form.cleaned_data['name'],
                level=form.cleaned_data['level'],
                email=form.cleaned_data['email'],
                phone=form.cleaned_data['phone'],
                password=make_password(form.cleaned_data['password']),
            )
            return redirect('school_login')
    else:
        form = SchoolSignupForm()

    return render(request, 'results/school_signup.html', {'form': form, 'error': error})


def school_login(request):
    error = None
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        school = School.objects.filter(email=email).first()

        if school and check_password(password, school.password):
            request.session['school_id'] = school.id
            return redirect('school_dashboard')
        else:
            error = "Invalid email or password"

    return render(request, 'results/school_login.html', {'error': error})


def school_dashboard(request):
    school_id = request.session.get('school_id')
    if not school_id:
        return redirect('school_login')

    school = get_object_or_404(School, id=school_id)
    students = Student.objects.filter(school=school)

    return render(request, 'results/school_dashboard.html', {'school': school, 'students': students})


def teacher_signup(request, school_id):
    school = get_object_or_404(School, id=school_id)
    error = None
    if request.method == 'POST':
        form = TeacherSignupForm(request.POST)
        if form.is_valid():
            Teacher.objects.create(
                school=school,
                full_name=form.cleaned_data['full_name'],
                email=form.cleaned_data['email'],
                phone=form.cleaned_data['phone'],
                password=make_password(form.cleaned_data['password']),
                grade=form.cleaned_data['grade'],
            )
            return redirect('teacher_login')
    else:
        form = TeacherSignupForm(initial={'school_id': school_id})

    return render(request, 'results/teacher_signup.html', {'form': form, 'school': school, 'error': error})


def teacher_login(request):
    error = None
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        teacher = Teacher.objects.filter(email=email).first()

        if teacher and check_password(password, teacher.password):
            request.session['teacher_id'] = teacher.id
            return redirect('teacher_dashboard')
        else:
            error = "Invalid email or password"

    return render(request, 'results/teacher_login.html', {'error': error})


def teacher_dashboard(request):
    teacher_id = request.session.get('teacher_id')
    if not teacher_id:
        return redirect('teacher_login')

    teacher = get_object_or_404(Teacher, id=teacher_id)
    students = Student.objects.filter(added_by=teacher)

    return render(request, 'results/teacher_dashboard.html', {'teacher': teacher, 'students': students})


def teacher_logout(request):
    request.session.flush()
    return redirect('teacher_login')


def teacher_add_student(request):
    teacher_id = request.session.get('teacher_id')
    if not teacher_id:
        return redirect('teacher_login')

    teacher = get_object_or_404(Teacher, id=teacher_id)
    error = None

    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        admission_number = request.POST.get('admission_number')
        stream = request.POST.get('stream', '')
        verification_code = request.POST.get('verification_code', '')

        Student.objects.create(
            school=teacher.school,
            added_by=teacher,
            full_name=full_name,
            admission_number=admission_number,
            grade=teacher.grade,
            stream=stream,
            verification_code=verification_code,
        )
        return redirect('teacher_dashboard')

    return render(request, 'results/teacher_add_student.html', {'teacher': teacher, 'error': error})


def add_mark(request):
    teacher_id = request.session.get('teacher_id')
    if not teacher_id:
        return redirect('teacher_login')

    teacher = get_object_or_404(Teacher, id=teacher_id)

    if request.method == 'POST':
        form = MarkForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_mark')
    else:
        form = MarkForm()
        form.fields['student'].queryset = Student.objects.filter(added_by=teacher)
        form.fields['subject'].queryset = Subject.objects.filter(school=teacher.school)
        form.fields['assessment'].queryset = Assessment.objects.filter(school=teacher.school)

    return render(request, 'results/add_mark.html', {'form': form})


def accountant_signup(request, school_id):
    school = get_object_or_404(School, id=school_id)
    error = None
    if request.method == 'POST':
        form = AccountantSignupForm(request.POST)
        if form.is_valid():
            Accountant.objects.create(
                school=school,
                full_name=form.cleaned_data['full_name'],
                email=form.cleaned_data['email'],
                phone=form.cleaned_data['phone'],
                password=make_password(form.cleaned_data['password']),
            )
            return redirect('accountant_login')
    else:
        form = AccountantSignupForm()

    return render(request, 'results/accountant_signup.html', {'form': form, 'school': school, 'error': error})


def accountant_login(request):
    error = None
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        accountant = Accountant.objects.filter(email=email).first()

        if accountant and check_password(password, accountant.password):
            request.session['accountant_id'] = accountant.id
            return redirect('accountant_dashboard')
        else:
            error = "Invalid email or password"

    return render(request, 'results/accountant_login.html', {'error': error})


def accountant_dashboard(request):
    accountant_id = request.session.get('accountant_id')
    if not accountant_id:
        return redirect('accountant_login')

    accountant = get_object_or_404(Accountant, id=accountant_id)
    students = Student.objects.filter(school=accountant.school)

    return render(request, 'results/accountant_dashboard.html', {'accountant': accountant, 'students': students})


def accountant_logout(request):
    request.session.flush()
    return redirect('accountant_login')


def add_fee_structure(request):
    accountant_id = request.session.get('accountant_id')
    if not accountant_id:
        return redirect('accountant_login')

    accountant = get_object_or_404(Accountant, id=accountant_id)
    error = None

    if request.method == 'POST':
        grade = request.POST.get('grade')
        term = request.POST.get('term')
        academic_year = request.POST.get('academic_year')
        amount_due = request.POST.get('amount_due')

        FeeStructure.objects.create(
            school=accountant.school,
            grade=grade,
            term=term,
            academic_year=academic_year,
            amount_due=amount_due,
        )
        return redirect('accountant_dashboard')

    return render(request, 'results/add_fee_structure.html', {'accountant': accountant, 'error': error})


def record_payment(request):
    accountant_id = request.session.get('accountant_id')
    if not accountant_id:
        return redirect('accountant_login')

    accountant = get_object_or_404(Accountant, id=accountant_id)
    students = Student.objects.filter(school=accountant.school)
    error = None

    if request.method == 'POST':
        student_id = request.POST.get('student')
        amount_paid = request.POST.get('amount_paid')
        date_paid = request.POST.get('date_paid')
        payment_method = request.POST.get('payment_method', '')
        reference_number = request.POST.get('reference_number', '')

        student = get_object_or_404(Student, id=student_id)

        Payment.objects.create(
            student=student,
            recorded_by=accountant,
            amount_paid=amount_paid,
            date_paid=date_paid,
            payment_method=payment_method,
            reference_number=reference_number,
        )
        return redirect('accountant_dashboard')

    return render(request, 'results/record_payment.html', {'accountant': accountant, 'students': students, 'error': error})


def download_report_card(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if not can_access_student(request, student):
        return redirect('home')

    marks = Mark.objects.filter(student=student)

    total = sum(m.score for m in marks)
    max_total = sum(m.max_score for m in marks)
    average = total / len(marks) if marks else 0
    percentage = (total / max_total * 100) if max_total else 0
    grade = get_grade(percentage)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{student.full_name}_report_card.pdf"'

    p = canvas.Canvas(response)
    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, 800, f"{student.school.name}")
    p.setFont("Helvetica", 12)
    p.drawString(50, 780, f"Report Card - {student.full_name}")
    p.drawString(50, 765, f"Admission No: {student.admission_number}  Grade: {student.grade}")

    y = 720
    p.drawString(50, y, "Subject")
    p.drawString(250, y, "Assessment")
    p.drawString(400, y, "Score")
    y -= 20

    for mark in marks:
        p.drawString(50, y, mark.subject.name)
        p.drawString(250, y, mark.assessment.name)
        p.drawString(400, y, f"{mark.score}/{mark.max_score}")
        y -= 20

    y -= 20
    p.drawString(50, y, f"Total: {total}")
    y -= 20
    p.drawString(50, y, f"Average: {average:.1f}")
    y -= 20
    p.drawString(50, y, f"Percentage: {percentage:.1f}%")
    y -= 20
    p.drawString(50, y, f"Grade: {grade}")

    p.showPage()
    p.save()
    return response


def download_fee_statement(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if not can_access_student(request, student):
        return redirect('home')

    fee_structure = FeeStructure.objects.filter(school=student.school, grade=student.grade).first()
    amount_due = fee_structure.amount_due if fee_structure else 0

    payments = Payment.objects.filter(student=student)
    total_paid = sum(p.amount_paid for p in payments)
    balance = amount_due - total_paid

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{student.full_name}_fee_statement.pdf"'

    p = canvas.Canvas(response)
    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, 800, f"{student.school.name}")
    p.setFont("Helvetica", 12)
    p.drawString(50, 780, f"Fee Statement - {student.full_name}")
    p.drawString(50, 765, f"Admission No: {student.admission_number}  Grade: {student.grade}")

    y = 720
    p.drawString(50, y, f"Amount Due: {amount_due}")
    y -= 20
    p.drawString(50, y, f"Total Paid: {total_paid}")
    y -= 20
    p.drawString(50, y, f"Balance: {balance}")
    y -= 40

    p.drawString(50, y, "Payment History")
    y -= 20
    for payment in payments:
        p.drawString(50, y, f"{payment.date_paid} - {payment.amount_paid} ({payment.payment_method})")
        y -= 20

    p.showPage()
    p.save()
    return response
def teacher_signup_select_school(request):
    schools = School.objects.all()
    if request.method == 'POST':
        school_id = request.POST.get('school')
        return redirect('teacher_signup', school_id=school_id)

    return render(request, 'results/select_school.html', {'schools': schools, 'role': 'Teacher', 'action_url': '/results/teacher/signup/select/'})


def accountant_signup_select_school(request):
    schools = School.objects.all()
    if request.method == 'POST':
        school_id = request.POST.get('school')
        return redirect('accountant_signup', school_id=school_id)

    return render(request, 'results/select_school.html', {'schools': schools, 'role': 'Accountant', 'action_url': '/results/accountant/signup/select/'})
def about_us(request):
    return render(request, 'results/about_us.html')


def our_services(request):
    return render(request, 'results/our_services.html') 
def delete_school_account(request):
    school_id = request.session.get('school_id')
    if not school_id:
        return redirect('school_login')

    school = get_object_or_404(School, id=school_id)
    school.delete()
    request.session.flush()
    return redirect('home')


def delete_teacher_account(request):
    teacher_id = request.session.get('teacher_id')
    if not teacher_id:
        return redirect('teacher_login')

    teacher = get_object_or_404(Teacher, id=teacher_id)
    teacher.delete()
    request.session.flush()
    return redirect('home')


def delete_accountant_account(request):
    accountant_id = request.session.get('accountant_id')
    if not accountant_id:
        return redirect('accountant_login')

    accountant = get_object_or_404(Accountant, id=accountant_id)
    accountant.delete()
    request.session.flush()
    return redirect('home')
def school_forgot_password(request):
    error = None
    success = None
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            school = School.objects.filter(email=email, phone=phone).first()
            if school:
                school.password = make_password(form.cleaned_data['new_password'])
                school.save()
                success = "Password reset successful. You can now log in."
                form = ForgotPasswordForm()
            else:
                error = "No account found with that email and phone number"
    else:
        form = ForgotPasswordForm()

    return render(request, 'results/forgot_password.html', {'form': form, 'error': error, 'success': success, 'role': 'School', 'login_url': '/results/school/login/'})


def teacher_forgot_password(request):
    error = None
    success = None
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            teacher = Teacher.objects.filter(email=email, phone=phone).first()
            if teacher:
                teacher.password = make_password(form.cleaned_data['new_password'])
                teacher.save()
                success = "Password reset successful. You can now log in."
                form = ForgotPasswordForm()
            else:
                error = "No account found with that email and phone number"
    else:
        form = ForgotPasswordForm()

    return render(request, 'results/forgot_password.html', {'form': form, 'error': error, 'success': success, 'role': 'Teacher', 'login_url': '/results/teacher/login/'})


def accountant_forgot_password(request):
    error = None
    success = None
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            accountant = Accountant.objects.filter(email=email, phone=phone).first()
            if accountant:
                accountant.password = make_password(form.cleaned_data['new_password'])
                accountant.save()
                success = "Password reset successful. You can now log in."
                form = ForgotPasswordForm()
            else:
                error = "No account found with that email and phone number"
    else:
        form = ForgotPasswordForm()

    return render(request, 'results/forgot_password.html', {'form': form, 'error': error, 'success': success, 'role': 'Accountant', 'login_url': '/results/accountant/login/'})


def parent_forgot_password(request):
    error = None
    success = None
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            parent = Parent.objects.filter(email=email, phone=phone).first()
            if parent:
                parent.password = make_password(form.cleaned_data['new_password'])
                parent.save()
                success = "Password reset successful. You can now log in."
                form = ForgotPasswordForm()
            else:
                error = "No account found with that email and phone number"
    else:
        form = ForgotPasswordForm()

    return render(request, 'results/forgot_password.html', {'form': form, 'error': error, 'success': success, 'role': 'Parent', 'login_url': '/results/parent/login/'})