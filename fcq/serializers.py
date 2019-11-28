from rest_framework import serializers


class ProfessorSerializer(serializers.Serializer):
    firstName = serializers.CharField()
    lastName = serializers.CharField()


class FcqSerializer(serializers.Serializer):
    # year = serializers.CharField()
    # semester = serializers.CharField()
    # section = serializers.CharField()
    # courseType = serializers.CharField()
    # online = serializers.CharField()
    # size = serializers.IntegerField()
    # numResponses = serializers.IntegerField()
    # challenge = serializers.FloatField()
    # learned = serializers.FloatField()
    # courseRating = serializers.FloatField()
    # profEffect = serializers.FloatField() #effectiveness of professor
    # profRating = serializers.FloatField()
    # courseSD = serializers.FloatField() #stand. dev. for course rating
    # profSD = serializers.FloatField() #stand. dev. for professor rating

    firstName = serializers.SerializerMethodField()
    lastName = serializers.SerializerMethodField()
    # department = serializers.SerializerMethodField()
    # course = serializers.SerializerMethodField()


    def get_firstName(self, obj):
        """ return the class' department code to be serialized """
        return obj.professor.firstName

    def get_lastName(self, obj):
        """ return the class' department code to be serialized """
        return obj.professor.lastName

    # def get_department(self, obj):
    #     """ return the class' department code to be serialized """
    #     return obj.course.department.code

    # def get_course(self, obj):
    #     """ return the class' department code to be serialized """
    #     return obj.course.course_subject