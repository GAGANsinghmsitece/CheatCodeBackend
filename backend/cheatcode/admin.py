from django.contrib import admin
from django.db import models
from cheatcode.models import Tag, Question
from  django.forms import CheckboxSelectMultiple

# Register your models here.
admin.site.register(Tag)

class QuestionModelAdmin(admin.ModelAdmin):
	formfield_overrides = {
		models.ManyToManyField:{'widget':CheckboxSelectMultiple}
	}

admin.site.register(Question,QuestionModelAdmin)