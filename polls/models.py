"""Django model for polls project."""
import datetime

from django.db import models
from django.utils import timezone


class Question(models.Model):
    """Question class for vote function."""

    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    end_date = models.DateTimeField('end date')

    def is_published(self):
        """To return date that published."""
        return timezone.now() >= self.pub_date

    def can_vote(self):
        """Check date that can vote."""
        return self.pub_date <= timezone.now() <= self.end_date

    def was_published_recently(self):
        """To return vote published recently."""
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    def __str__(self):
        """To return question text."""
        return self.question_text


class Choice(models.Model):
    """Class for choice."""

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        """To return choice text."""
        return self.choice_text
