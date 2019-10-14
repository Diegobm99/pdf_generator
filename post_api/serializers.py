from rest_framework import serializers

class HelloSerializers(serializers.Serializer):
    """Serializes a name field for testing our APIView"""
    name = serializers.CharField(max_length=10)
    cpf = serializers.CharField(max_length=11)

class csv_input(serializers.Serializer):
    """Serializes a name field for testing our APIView"""
    name = serializers.CharField(max_length=10)
    cpf = serializers.CharField(max_length=11)
