from django.urls import path, include
from examsapp.views.user_views import *
from examsapp.views.course_exam_views import *
from examsapp.views.question_exam_views import *
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from examsapp.views.ocr_view import trigger_question_extraction

router = DefaultRouter()
router.register('courses', CourseViewSet, basename='course')
router.register('profile', UserProfileView, basename='profile') 
router.register('exams', ExamViewSet, basename='exam')
router.register(r'exams/(?P<exam_id>[^/.]+)/questions', QuestionPerExamViewSet, 
basename='exam-questions')

router.register(r'exams/(?P<exam_id>\d+)/questions', QuestionPerExamViewsetForAnswerGeneration, basename='questions')


router.register('lecturer-course', CoursePerLecturerViewSet, basename='lecturer-course')

urlpatterns = [
    path('', include(router.urls)),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('student-register/', StudentRegistrationView.as_view(), name='student-register'),

    path('questions/', QuestionListView.as_view(), name='questions'),
    path('answers/', AnswerCreateView.as_view(), name='answers'),

    path('trigger-ocr-question-extraction/', trigger_question_extraction, name='trigger-ocr'),
]
