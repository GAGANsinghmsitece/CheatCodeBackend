from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework import generics,status
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from cheatcode.reader import UpdateInfo
from cheatcode.models import Tag, Question
from cheatcode.serializers import TagSerializer, QuestionSerializer
from cheatcode.exceptions import TagDoesNotExist

class Pagination(PageNumberPagination):
	page_size = 25
	page_size_query_param = 'page'

# Create your views here.
def home_page(request):
	UpdateInfo()
	return HttpResponse('<b>Welcome to CheatCode</b>')

class TagList(generics.ListAPIView):
	queryset = Tag.objects.all()
	serializer_class = TagSerializer

class QuestionList(generics.ListAPIView):
	queryset = Question.objects.all().prefetch_related('tags')
	serializer_class = QuestionSerializer
	pagination_class = Pagination

class QuestionsByTagList(generics.ListAPIView):
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