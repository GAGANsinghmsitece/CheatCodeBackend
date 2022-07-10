from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext as _


# Create your models here.
class Tag(models.Model):
	name = models.CharField(max_length=100,unique=True,blank=False,null=False)

	def __str__(self):
		return self.name

class Question(models.Model):

	class Diffculty(models.TextChoices):
		EASY = '1',_('Easy')
		MEDIUM = '2', _('Medium')
		Hard = '3', _('Hard')

	heading = models.CharField(max_length=300)
	description = models.TextField()
	difficulty = models.CharField(max_length=1,choices=Diffculty.choices)
	like = models.IntegerField()
	unlike = models.IntegerField()
	tags = models.ManyToManyField(Tag)
	link = models.CharField(max_length=300,unique=True,blank=False)

	def __str__(self):
		return self.heading

class Profile(models.Model):
	name = models.CharField(max_length=100,null=False,blank=False)
	user = models.OneToOneField(User, on_delete=models.CASCADE,primary_key=True)
	bio = models.TextField(max_length=300,blank=True,null=False)
	completed = models.ManyToManyField(Question)

@receiver(post_save,sender=User)
def update_user_profile(sender,instance,created,**kwargs):
	if created:
		Profile.objects.create(user=instance)
	instance.profile.save()