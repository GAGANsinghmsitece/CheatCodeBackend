from django.forms import ModelForm
from django import forms
from cheatcode.models import Tag, Question

nameError={
	"field":"name",
	"error":"This tag already exists"
}

class TagForm(ModelForm):
	name = forms.CharField(max_length=100)

	class Meta:
		model = Tag
		fields = ['name']

	def clean(self):
		if 'name' in self.cleaned_data:
			name = self.cleaned_data['name']
			print(name)
			if Tag.objects.filter(name__iexact=name).exists():
				self.add_error(nameError["field"], nameError["error"])
		return self.cleaned_data

class ProblemForm(ModelForm):
	heading = forms.CharField(max_length=300,required=True)
	description = forms.Textarea()
	like = forms.IntegerField(required=True)
	unlike = forms.IntegerField(required=True)
	tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(),required=True)
	link = forms.CharField(required=True,max_length=300)


	class Meta:
		model = Question
		fields = ['heading','description','difficulty','like','unlike','tags','link']