from rest_framework import serializers


class PrerequisiteSerializer(serializers.Serializer):

    requiredNumber = serializers.IntegerField()
    possibleClasses = serializers.ListField(child=serializers.CharField())

    classId = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    auditId = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
