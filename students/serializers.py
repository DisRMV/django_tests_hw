from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.db.models import Count

from students.models import Course
from django.conf import settings


class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = ("id", "name", "students")

    def validate(self, data):
        message = 'Too many students per course. Max count 20'
        method = self.context['request'].method
        if (method == 'POST' or method == 'PUT') and len(data['students']) > settings.MAX_STUDENTS_PER_COURSE:
            raise ValidationError(detail=message)
        if method == 'PATCH' and data.get('students'):
            instance_id = self.instance.id
            students_per_course = Course.objects.filter(id=instance_id).annotate((Count('students')))
            quantity = len(data['students']) + students_per_course[0].students__count
            if quantity > settings.MAX_STUDENTS_PER_COURSE:
                raise ValidationError(detail=message)
        return data
