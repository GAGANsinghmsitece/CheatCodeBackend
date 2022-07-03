from rest_framework import serializers
from cheatcode.models import Tag, Question



class TagSerializer(serializers.ModelSerializer):
	class Meta:
		model = Tag
		fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):
	tags = TagSerializer(many=True,read_only =True)
	class Meta:
		model = Question
		fields = '__all__'
