from django.contrib import admin, messages
from .models import User, Roles, Course, Exam, CollegeCampus, CampusSchool, CampusDepartment, Question
from .ocr_utils import extract_questions_from_pdf


# Register your models here.
admin.site.register(User)
admin.site.register(Course)
admin.site.register(Question)
# admin.site.register(LecturerAnswerSheet)
# admin.site.register(StudentAnswerSheet)
# admin.site.register(LecturerAnswer)
# admin.site.register(StudentAnswer)
admin.site.register(CollegeCampus)
admin.site.register(CampusSchool)
admin.site.register(CampusDepartment)


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'date', 'created_by')
    actions = ['extract_questions']

    def extract_questions(self, request, queryset):
        for exam in queryset:
            try:
                extract_questions_from_pdf(exam)
                self.message_user(request, f"Extracted questions for: {exam}", messages.SUCCESS)
            except Exception as e:
                self.message_user(request, f"Failed to extract for {exam}: {e}", messages.ERROR)

    extract_questions.short_description = "Extract questions from exam PDF"

