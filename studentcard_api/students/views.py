from django.shortcuts import render, redirect, get_object_or_404
from .models import Student
from .forms import StudentForm

def student_list(request):
    students = Student.objects.all()

    # Filters
    student_class = request.GET.get('student_class')
    min_marks = request.GET.get('min_marks')
    max_marks = request.GET.get('max_marks')
    ordering = request.GET.get('ordering')

    if student_class:
        students = students.filter(student_class=student_class)

    if min_marks:
        students = students.filter(marks__gte=min_marks)

    if max_marks:
        students = students.filter(marks__lte=max_marks)

    if ordering:
        students = students.order_by(ordering)

    return render(request, 'students/students_list.html', {'students': students})


def student_form(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('student-list')
    else:
        form = StudentForm()
    return render(request, 'students/students_form.html', {'form': form})


def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        student.delete()
        return redirect('student-list')
    return render(request, 'students/students_confirm_delete.html', {'student': student})
