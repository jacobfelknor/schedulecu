from rest_framework import serializers

# not 200% sure this is correct. Just need the serializer to hold the possibleClasses field


class PrerequisiteSerializer(serializers.Serializer):

    requiredNumber = serializers.IntegerField()
    possibleClasses = serializers.ListField(child=serializers.CharField())

    classId = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    auditId = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
