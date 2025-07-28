from rest_framework import viewsets
from rest_framework import permissions
from examsapp.models.course_exam_model import Course, Exam
from examsapp.serializers.course_exam_serializer import CourseSerializer, ExamSerializer

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes  = [permissions.IsAuthenticated]

class ExamViewSet(viewsets.ModelViewSet):
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer
    permission_classes = [permissions.IsAuthenticated]


class CoursePerLecturerViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Course.objects.filter(lecturer=user)