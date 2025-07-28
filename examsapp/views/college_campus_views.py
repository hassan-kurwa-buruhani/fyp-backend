from django.shortcuts import render
from rest_framework import viewsets
from examsapp.models import CollegeCampus, CampusSchool, campusDepartment
from examsapp.serializers import CollegeCampusSerializer, CampusSchoolSerializer, campusDepartmentSerializer
from rest_framework.permissions import IsAuthenticated

class CollegeCampusViewSet(viewsets.ModelViewSet):
    queryset = CollegeCampus.objects.all()
    serializer_class = CollegeCampusSerializer
    permission_classes = [IsAuthenticated]

class CampusSchoolViewSet(viewsets.ModelViewSet):
    queryset = CampusSchool.objects.all()
    serializer_class = CampusSchoolSerializer
    permission_classes = [IsAuthenticated]

class campusDepartmentViewSet(viewsets.ModelViewSet):
    queryset = campusDepartment.objects.all()
    serializer_class = campusDepartmentSerializer
    permission_classes = [IsAuthenticated]