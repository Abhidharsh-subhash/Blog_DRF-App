from rest_framework.validators import ValidationError
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from .models import User

class SignUpSerializer(serializers.ModelSerializer):
    email=serializers.CharField(max_length=80)
    username=serializers.CharField(max_length=45)
    #write_only is used to keep our password private
    password=serializers.CharField(min_length=8,write_only=True)
    class Meta:
        model=User
        # fields = '__all__'  # if you need to specify all the fields in the model
        fields=['email','username','password']
    def validate(self, attrs):
        email_exists=User.objects.filter(email=attrs['email']).exists()
        if email_exists:
            raise ValidationError('Email has already been used')
        return super().validate(attrs)
    #custom create method to hash the passwords of the users
    def create(self, validated_data):
        password=validated_data.pop('password')
        user=super().create(validated_data)
        user.set_password(password)
        user.save()
        Token.objects.create(user=user)
        return user
    
