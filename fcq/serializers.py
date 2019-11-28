from rest_framework import serializers


class ProfessorSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    firstName = serializers.CharField()
    lastName = serializers.CharField()