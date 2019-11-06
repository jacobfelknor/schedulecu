from rest_framework import serializers


class TeacherSerializer(serializers.Serializer):
    name = serializers.CharField()
    mainDepartment = serializers.CharField()

    numClasses = serializers.IntegerField() #how many classes teacher has taught        
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