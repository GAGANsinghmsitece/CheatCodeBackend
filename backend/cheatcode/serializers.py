from rest_framework import serializers
from cheatcode.models import Tag, Question, Profile
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password


class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ['username','email']

class TagSerializer(serializers.ModelSerializer):
	class Meta:
		model = Tag
		fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):
	tags = TagSerializer(many=True,read_only =True)
	class Meta:
		model = Question
		fields = '__all__'

class QuestionWithoutTagsSerializer(serializers.ModelSerializer):
	class Meta:
		model = Question
		exclude = ['tags']

class ProfileSerializer(serializers.ModelSerializer):
	user = UserSerializer(required=True)
	class Meta:
		model = Profile
		exclude = ['completed']

class SubmittedSerializer(serializers.Serializer):
	question_id = serializers.IntegerField()


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email']
        )

        
        user.set_password(validated_data['password'])
        user.save()

        return user