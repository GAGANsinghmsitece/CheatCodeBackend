from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework import generics,status
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.contrib.auth.models import User

from cheatcode.reader import UpdateInfo
from cheatcode.models import Tag, Question, Profile
from cheatcode.serializers import TagSerializer, QuestionSerializer, SubmittedSerializer, ProfileSerializer, QuestionWithoutTagsSerializer, RegisterSerializer
from cheatcode.exceptions import TagDoesNotExist, InvalidQuestion, InvalidRequest, UserDoesNotExist

class CustomPagination(LimitOffsetPagination):
	default_limit = 25
	max_limit = 25

class Pagination(PageNumberPagination):
    page_size = 25
    page_size_query_param = 'page_size'
    max_page_size = 25

# Create your views here.
def home_page(request):
	#UpdateInfo()
	return HttpResponse('<b>Welcome to CheatCode</b>')

class TagList(generics.ListAPIView):
	permission_classes = (IsAuthenticated,)
	queryset = Tag.objects.all()
	serializer_class = TagSerializer


class QuestionList(generics.ListAPIView):
	permission_classes = (IsAuthenticated,)
	queryset = Question.objects.all().prefetch_related('tags')
	serializer_class = QuestionSerializer
	pagination_class = Pagination

class QuestionsByTagList(generics.ListAPIView):
	permission_classes = (IsAuthenticated,)
	serializer_class = QuestionSerializer
	pagination_class = Pagination
	lookup_param = 'id'

	def get_queryset(self):
		tagid = self.kwargs.get(self.lookup_param)
		try:
			queryset =  Tag.objects.get(id=tagid).question_set.all()
			return queryset 
		except:
			raise TagDoesNotExist()

class SubmitQuestion(APIView):
	serializer_class = SubmittedSerializer
	permission_classes = (IsAuthenticated,)

	def post(self,request):
		valid_data = self.serializer_class(data=request.data)
		if valid_data.is_valid():
			try:
				user_profile = request.user.profile
				question_id = request.data['question_id']
				if user_profile.completed.filter(id=question_id).exists():
					user_profile.completed.remove(question_id)
					return Response({'status':200,'success':True,'message':'The question is marked as unsolved'})
				else:
					user_profile.completed.add(question_id)
					return Response({'status':200,'success':True,'message':'The question is marked as completed'})
			except:
				raise InvalidQuestion()
		else:
			raise InvalidRequest()

class UserDetails(generics.ListAPIView):
	permission_classes = (IsAuthenticated,)
	serializer_class = ProfileSerializer
	lookup_param = 'username'

	def get_queryset(self):
		try:
			username = self.kwargs.get(self.lookup_param)
			if User.objects.filter(username=username).exists():
				return Profile.objects.filter(user__username=username).select_related('user')
			else:
				raise UserDoesNotExist()
		except:
			raise InvalidRequest()

class CompletedQuestions(generics.ListAPIView):
	permission_classes = (IsAuthenticated,)
	serializer_class = QuestionWithoutTagsSerializer
	pagination_class = Pagination
	lookup_param = 'username'

	def get_queryset(self):
		username = self.kwargs.get(self.lookup_param)
		if User.objects.filter(username=username).exists():
			return Question.objects.filter(profile__user__username = username)
		else:
			raise UserDoesNotExist()

class UserSignup(generics.CreateAPIView):
	queryset = User.objects.all()
	serializer_class = RegisterSerializer