from django.contrib import admin
from django.db import models
from cheatcode.models import Tag, Question, Profile
from  django.forms import CheckboxSelectMultiple

# Register your models here.
admin.site.register(Tag)
admin.site.register(Profile)

class QuestionModelAdmin(admin.ModelAdmin):
	formfield_overrides = {
		models.ManyToManyField:{'widget':CheckboxSelectMultiple}
	}

admin.site.register(Question,QuestionModelAdmin)