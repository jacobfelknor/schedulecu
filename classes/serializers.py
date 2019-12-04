from rest_framework import serializers


class SectionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    section_number = serializers.CharField()
    session = serializers.CharField()
    class_number = serializers.IntegerField()
    credit = serializers.CharField()
    class_component = serializers.CharField()
    start_time = serializers.CharField()
    end_time = serializers.CharField()
    days = serializers.CharField()
    building_room = serializers.CharField()
    max_enrollment = serializers.IntegerField()
    campus = serializers.CharField()
    course_id = serializers.SerializerMethodField()
    department = serializers.SerializerMethodField()
    course_subject = serializers.SerializerMethodField()
    course_title = serializers.SerializerMethodField()
    num_sections = serializers.SerializerMethodField()

    def get_course_id(self, obj):
        """ return the class' department code to be serialized """
        return obj.parent_class.id

    def get_department(self, obj):
        """ return the class' department code to be serialized """
        return obj.parent_class.department.code

    def get_course_subject(self, obj):
        """ return the class' department code to be serialized """
        return obj.parent_class.course_subject

    def get_course_title(self, obj):
        """ return the class' department code to be serialized """
        return obj.parent_class.course_title

    def get_num_sections(self, obj):
        """ return the class' department code to be serialized """
        return obj.parent_class.sections.count()


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
