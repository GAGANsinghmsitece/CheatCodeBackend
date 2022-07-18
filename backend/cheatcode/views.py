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
from django.db.models import Case, When, Value, BooleanField, Count
from django.db.models.functions.comparison import NullIf

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import EmailMessage
from django.conf import settings

from cheatcode.reader import UpdateInfo
from cheatcode.models import Tag, Question, Profile
from cheatcode.serializers import TagSerializer, QuestionSerializer, SubmittedSerializer, ProfileSerializer, QuestionWithoutTagsSerializer, RegisterSerializer
from cheatcode.exceptions import TagDoesNotExist, InvalidQuestion, InvalidRequest, UserDoesNotExist, InvalidParamter

@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    """
    Handles password reset tokens
    When a token is created, an e-mail needs to be sent to the user
    :param sender: View Class that sent the signal
    :param instance: View Instance that sent the signal
    :param reset_password_token: Token Model Object
    :param args:
    :param kwargs:
    :return:
    """
    # send an e-mail to the user
    context = {
        'current_user': reset_password_token.user,
        'username': reset_password_token.user.username,
        'email': reset_password_token.user.email,
        'reset_password_url': "{}?token={}".format(
            instance.request.build_absolute_uri(reverse('password_reset:reset-password-confirm')),
            reset_password_token.key)
    }
    mail_subject = "CheatCode:- Reset your password"
    message = render_to_string("email/password_reset.html",context)
    email_to = context['email']
    email = EmailMessage(mail_subject,message,to=[email_to])
    email.content_subtype = "html"
    email.send()
    # render email text
    #email_html_message = render_to_string('email/user_reset_password.html', context)
    #email_plaintext_message = render_to_string('email/user_reset_password.txt', context)
    

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
	serializer_class = QuestionSerializer
	pagination_class = Pagination

	def get_queryset(self):
		difficulty_level = self.request.GET.get('difficulty',None)
		if difficulty_level == None:
			completed_questions = Question.objects.filter(profile=self.request.user.profile)
			all_questions = Question.objects.annotate(is_complete=Case(
				When(
					pk__in=completed_questions.values('pk'), 
					then=Value(True)
				),
				default=Value(False), 
				output_field=BooleanField())
			).prefetch_related('tags')
			return all_questions
		elif difficulty_level == "1" or difficulty_level == "2" or difficulty_level=="3":
			completed_questions = Question.objects.filter(profile=self.request.user.profile)
			all_questions = Question.objects.filter(difficulty=difficulty_level).annotate(is_complete=Case(
				When(
					pk__in=completed_questions.values('pk'), 
					then=Value(True)
				),
				default=Value(False), 
				output_field=BooleanField())
			).prefetch_related('tags')
			return all_questions
		else:
			raise InvalidParamter()

class TopQuestionList(generics.ListAPIView):
	permission_classes = (IsAuthenticated,)
	serializer_class = QuestionSerializer
	pagination_class = Pagination

	def get_queryset(self):
		difficulty_level = self.request.GET.get('difficulty',None)
		if difficulty_level == None:
			completed_questions = Question.objects.filter(profile=self.request.user.profile)
			all_questions = Question.objects.all().annotate(is_complete=Case(
				When(
					pk__in=completed_questions.values('pk'), 
					then=Value(True)
				),
				default=Value(False), 
				output_field=BooleanField()),
				votes_difference=Count('like')-Count('unlike'),
			).order_by('votes_difference').prefetch_related('tags')
			print(all_questions)
			return all_questions
		elif difficulty_level == "1" or difficulty_level == "2" or difficulty_level=="3":
			completed_questions = Question.objects.filter(profile=self.request.user.profile)
			all_questions = Question.objects.filter(difficulty=difficulty_level).annotate(is_complete=Case(
				When(
					pk__in=completed_questions.values('pk'), 
					then=Value(True)
				),
				default=Value(False), 
				output_field=BooleanField()),
				votes_difference=Count('like')-Count('unlike'),
			).order_by('votes_difference').prefetch_related('tags')
			return all_questions
		else:
			raise InvalidParamter()

class QuestionsByTagList(generics.ListAPIView):
	permission_classes = (IsAuthenticated,)
	serializer_class = QuestionSerializer
	pagination_class = Pagination
	lookup_param = 'id'

	def get_queryset(self):
		try:
			tagid = self.kwargs.get(self.lookup_param)
			queryset =  Question.objects.filter(tag__id=tagid).annotate(is_complete=Case(
				When(
					pk__in=completed_questions.values('pk'), 
					then=Value(True)
				),
				default=Value(False), 
				output_field=BooleanField())
			).prefetch_related('tags')

			return queryset
		except:
			TagDoesNotExist()

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