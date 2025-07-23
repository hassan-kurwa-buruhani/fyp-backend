from django.db import models
from .user_model import User
from .course_exam_model import Exam

class LecturerAnswerSheet(models.Model):
    lecturer = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'Lecturer'})
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='answer_sheets/lecturers_sheets/')
    answer_sheet_group_id = models.CharField(max_length=100, help_text="ID for the answer sheet", null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    ocr_processed = models.BooleanField(default=False)

    class Meta:
        ordering = ['answer_sheet_group_id']
        unique_together = ('lecturer', 'exam', 'answer_sheet_group_id')

    def __str__(self):
        return f"{self.lecturer.first_name} {self.lecturer.last_name} - {self.exam.title} ({self.exam.course.code} - {self.exam.course.name})"

class StudentAnswerSheet(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'Student'})
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='answer_sheets/students/')
    booklet_page_number = models.PositiveIntegerField(help_text="Page number in the student's booklet", null=True, blank=True)
    booklet_group_id = models.CharField(max_length=100, help_text="Group ID for booklet pages", null=True, blank=True)

    uploaded_at = models.DateTimeField(auto_now_add=True)
    ocr_processed = models.BooleanField(default=False)

    class Meta:
        ordering = ['booklet_group_id', 'booklet_page_number']
        unique_together = ('student', 'exam', 'booklet_group_id', 'booklet_page_number')


    def __str__(self):
        return f"{self.student.first_name} {self.student.last_name} - {self.exam.title} ({self.exam.course.code} - {self.exam.course.name})"
