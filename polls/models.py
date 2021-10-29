"""Models for KU-poll."""
import datetime

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Question(models.Model):
    """Class that contain question option."""

    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    end_date = models.DateTimeField('end date')

    def __str__(self):
        """To return a question_text."""
        return self.question_text

    def is_published(self):
        """To return is the question available."""
        return timezone.now() >= self.pub_date

    def can_vote(self):
        """To check that question can vote or not."""
        return self.pub_date <= timezone.now() <= self.end_date

    def was_published_recently(self):
        """To check that question just open or not."""
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'


class Choice(models.Model):
    """Class that contain choice option."""

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)


    def __str__(self):
        """To return choice_text."""
        return self.choice_text

    @property
    def votes(self):
        return  self.question.vote_set.filter(choice=self).count

class Vote(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)