from rest_framework import serializers


class TeacherSerializer(serializers.Serializer):
    name = serializers.CharField()
    mainDepartment = serializers.CharField()
    numClasses = serializers.IntegerField() 
    avgClassSize = serializers.IntegerField()
    avgInstRating = serializers.FloatField()
    avgCourseRating = serializers.FloatField()
    avgChallenge = serializers.FloatField()
    courseList = serializers.ListField(child=serializers.CharField())
    timesCourseTaught = serializers.ListField(child=serializers.IntegerField())
    courseRating = serializers.ListField(child=serializers.FloatField())
    courseInstRating = serializers.ListField(child=serializers.FloatField())
    courseChallenge = serializers.ListField(child=serializers.FloatField())
    classIndex = serializers.ListField(child=serializers.IntegerField())



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