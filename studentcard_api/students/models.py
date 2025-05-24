from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    student_class = models.CharField(max_length=20)
    roll_no = models.IntegerField(unique=True)
    marks = models.FloatField()

    def __str__(self):
        return self.name
