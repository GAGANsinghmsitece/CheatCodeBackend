import os
import json

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from cheatcode.models import Tag, Question
from cheatcode.forms import TagForm, ProblemForm

LEETCODE_FILE_PATH = os.path.dirname(__file__)+'/../../crawler/data.json'

def UpdateInfo():
	f = open(LEETCODE_FILE_PATH)
	data = json.loads(f.read())
	tags = data["tags"]


	for t in tags:
		form = TagForm({'name':t['name']})
		if form.is_valid():
			form.save()
		else:
			print(form.errors)

	problems = data['problems']

	for p in problems:
		diff = '1'
		if p['difficulty'] == "Medium":
			diff = '2'
		elif p['difficulty'] == "Hard":
			diff = '3'

		taglist = []
		for t in p["tags"]:
			taglist.append(t["name"])


		tag_set = Tag.objects.filter(name__in=taglist)

		initialdata={
			'heading':p['heading'],
			'description':p['description'],
			'difficulty':diff,
			'like':int(p['like']),
			'unlike':int(p['unlike']),
			'tags':tag_set
		}

		if Question.objects.filter(heading=initialdata['heading']).exists():
			form = ProblemForm(initialdata,instance=Question.objects.get(heading=initialdata['heading']))
			if form.is_valid():
				form.save()
			else:
				print(form.errors)
		else:
			form = ProblemForm(initialdata)
			if form.is_valid():
				form.save()
			else:
				print(form.errors)

UpdateInfo()