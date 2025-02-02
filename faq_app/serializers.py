from rest_framework import serializers
from .models import FAQ

class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = '__all__'

    def validate_question(self, value):
        if not value.strip():
            raise serializers.ValidationError("This field may not be blank.")
        return value
