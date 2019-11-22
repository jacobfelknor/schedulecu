from rest_framework import serializers


class SectionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    department = (
        serializers.SerializerMethodField()
    )  # since this is now a foreign key relationship
    course_subject = serializers.SerializerMethodField()
    section_number = serializers.CharField()
    session = serializers.CharField()
    class_number = serializers.IntegerField()
    credit = serializers.CharField()
    course_title = serializers.SerializerMethodField()
    class_component = serializers.CharField()
    start_time = serializers.CharField()
    end_time = serializers.CharField()
    days = serializers.CharField()
    building_room = serializers.CharField()
    instructor_name = serializers.CharField()
    max_enrollment = serializers.IntegerField()
    campus = serializers.CharField()

    def get_department(self, obj):
        """ return the class' department code to be serialized """
        return obj.parent_class.department.code

    def get_course_subject(self, obj):
        return obj.parent_class.course_subject

    def get_course_title(self, obj):
        return obj.parent_class.course_title


class ClassSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    department = serializers.SerializerMethodField()
    course_title = serializers.CharField()
    course_subject = serializers.IntegerField()
    num_sections = serializers.SerializerMethodField()

    def get_department(self, obj):
        """ return the class' department code to be serialized """
        return obj.department.code

    def get_num_sections(self, obj):
        return obj.sections.count()
