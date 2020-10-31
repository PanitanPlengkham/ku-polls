import datetime

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from polls.models import Question


def create_question(question_text, days):
    """Class for create question.

    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time, end_date=time)


class QuestionModelTests(TestCase):
    """Class test for Model."""

    def test_was_published_recently_with_old_question(self):
        """was_published_recently() returns False for questions whose pub_date is older than 1 day."""
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """Function test.

        was_published_recently() returns True for questions whose pub_date
        is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

    def test_was_published_recently_with_future_question(self):
        """Function test.

        was_published_recently() returns False for questions whose pub_date
        is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_is_published_with_past_question(self):
        """Returns true if current date is on or after question’s publication date."""
        time = timezone.now() - datetime.timedelta(days=2)
        past_question = Question(pub_date=time)
        self.assertIs(past_question.is_published(), True)

    def test_is_published_with_future_question(self):
        """is_published return false when polls is not open yet.(published is in future)."""
        time = timezone.now() + datetime.timedelta(hours=2)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.is_published(), False)

    def test_can_vote_with_past_question(self):
        """can_vote return false when polls are close already(end_date is in past and pub_date too)."""
        time = timezone.now() - datetime.timedelta(days=4)
        end_time = timezone.now() - datetime.timedelta(days=2)
        past_question = Question(pub_date=time, end_date=end_time)
        self.assertIs(past_question.can_vote(), False)

    def test_can_vote_with_future_question(self):
        """can_vote return false when polls are not open yet.(end_date is in future and pub_date too)."""
        time = timezone.now() + datetime.timedelta(days=2)
        end_time = timezone.now() + datetime.timedelta(days=4)
        future_question = Question(pub_date=time, end_date=end_time)
        self.assertIs(future_question.can_vote(), False)