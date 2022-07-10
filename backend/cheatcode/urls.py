from rest_framework_simplejwt import views as jwt_views 
from django.urls import path
from cheatcode import views

urlpatterns =[
	path('',views.home_page,name='HomePage'),
	path('token',jwt_views.TokenObtainPairView.as_view(),name='GetToken'),
	path('token/refresh',jwt_views.TokenRefreshView.as_view(),name='GetRefreshToken'),
	path('tags',views.TagList.as_view(),name='TagList'),
	path('questions',views.QuestionList.as_view(),name='QuestionList'),
	path('tags/<int:id>',views.QuestionsByTagList.as_view(),name='QuestionsByTagList'),
	path('completed',views.SubmitQuestion.as_view(),name='SubmitQuestion'),
	path('user/<slug:username>',views.UserDetails.as_view(),name='UserDetail'),
	path('user/<slug:username>/completed',views.CompletedQuestions.as_view(),name='UserDetailCompleted'),
	path('signup',views.UserSignup.as_view(),name='UserSignup')
]