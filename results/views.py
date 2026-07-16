from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.hashers import make_password, check_password
from .models import Student, Mark, FeeStructure, Payment, Parent
from .forms import MarkForm, ParentSignupForm


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


def student_results(request, student_id):
    student = get_object_or_404(Student, id=student_id)
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


def student_list(request):
    students = Student.objects.all()
    return render(request, 'results/student_list.html', {'students': students})


def student_fees(request, student_id):
    student = get_object_or_404(Student, id=student_id)

    fee_structure = FeeStructure.objects.filter(grade=student.grade).first()
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
    if request.method == 'POST':
        phone = request.POST.get('phone')
        password = request.POST.get('password')

        parent = Parent.objects.filter(phone=phone).first()

        if parent and check_password(password, parent.password):
            request.session['parent_id'] = parent.id
            return redirect('parent_dashboard')
        else:
            error = "Invalid phone or password"

    return render(request, 'results/parent_login.html', {'error': error})


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


def add_mark(request):
    if request.method == 'POST':
        form = MarkForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_mark')
    else:
        form = MarkForm()

    return render(request, 'results/add_mark.html', {'form': form})


def parent_signup(request):
    error = None
    if request.method == 'POST':
        form = ParentSignupForm(request.POST)
        if form.is_valid():
            admission_number = form.cleaned_data['admission_number']
            verification_code = form.cleaned_data['verification_code']

            student = Student.objects.filter(
                admission_number=admission_number,
                verification_code=verification_code
            ).first()

            if student:
                parent = Parent.objects.create(
                    full_name=form.cleaned_data['full_name'],
                    phone=form.cleaned_data['phone'],
                    email=form.cleaned_data['email'],
                    password=make_password(form.cleaned_data['password']),
                )
                parent.students.add(student)
                return redirect('parent_login')
            else:
                error = "Admission number or verification code is incorrect"
    else:
        form = ParentSignupForm()

    return render(request, 'results/parent_signup.html', {'form': form, 'error': error})