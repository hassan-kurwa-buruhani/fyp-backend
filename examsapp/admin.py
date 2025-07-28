from django.contrib import admin, messages
from .models import User, Question,Roles, Course, Exam, CollegeCampus, CampusSchool, CampusDepartment, Answer
from .ocr_utils import extract_questions_from_pdf
from django.utils.html import format_html


# Register your models here.
admin.site.register(User)
admin.site.register(Course)
admin.site.register(Answer)
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



# from django.contrib import admin
# from django.utils.html import format_html
# from .models import Question

# @admin.register(Question)
# class QuestionAdmin(admin.ModelAdmin):
#     list_display = ['exam', 'question_number', 'short_question']
#     readonly_fields = ['ai_answer_preview']

#     def short_question(self, obj):
#         return obj.question_text[:50]
#     short_question.short_description = "Question"

#     def ai_answer_preview(self, obj):
#         return format_html(
#             '''
#             <div id="answer-{id}">Loading...</div>
#             <script src="https://js.puter.com/v2/"></script>
#             <script>
#                 puter.ai.chat("{text}", {{ model: "gpt-4.1-nano" }})
#                     .then(response => {{
#                         document.getElementById("answer-{id}").innerText = response;
#                     }});
#             </script>
#             ''',
#             id=obj.id,
#             text=obj.question_text.replace('"', '\\"')
#         )
#     ai_answer_preview.short_description = "AI Answer Preview"


