from django.contrib.auth.models import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 
            'email', 
            'password')
        extra_kwargs = {'password' : {'write_only' : True}}

    # Чтобы иметь возможность возвращать полные экземпляры объекта 
    # на основе проверенных данных, нам необходимо реализовать метод create
    def create(self, validated_data): # переопределим метод 
        user = User(
            email = validated_data['email'],
            username = validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

