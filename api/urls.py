from django.urls import path, include
from examsapp.views.user_views import *
from examsapp.views.course_exam_views import *
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

router = DefaultRouter()
router.register('courses', CourseViewSet, basename='course')
router.register('profile', UserProfileView, basename='profile') 
router.register('exams', ExamViewSet, basename='exam')
router.register('lecturer-course', CoursePerLecturerViewSet, basename='lecturer-course')

urlpatterns = [
    path('', include(router.urls)),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('student-register/', StudentRegistrationView.as_view(), name='student-register'),
]
