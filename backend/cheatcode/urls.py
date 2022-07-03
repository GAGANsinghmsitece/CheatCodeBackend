from django.urls import path
from cheatcode import views

urlpatterns =[
	path('',views.home_page,name='HomePage'),
	path('tags',views.TagList.as_view(),name='TagList'),
	path('questions',views.QuestionList.as_view(),name='QuestionList'),
	path('tags/<int:id>',views.QuestionsByTagList.as_view(),name='QuestionsByTagList')
]