from rest_framework import serializers


class ProfessorSerializer(serializers.Serializer):
    firstName = serializers.CharField()
    lastName = serializers.CharField()

class FcqSerializer(serializers.Serializer):
    index = serializers.IntegerField()
    year = serializers.CharField()
    semester = serializers.CharField()
    department = serializers.CharField()
    subject = serializers.CharField()
    course = serializers.CharField()
    section = serializers.CharField()
    course_title = serializers.CharField()
    courseType = serializers.CharField()
    level = serializers.CharField()
    online = serializers.CharField()
    size = serializers.IntegerField()