"""Model for KU-polls."""
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.dispatch import receiver
from .settings import LOGGING
import logging

from .models import Question, Choice, Vote
logging.config.dictConfig(LOGGING)
logger = logging.getLogger('polls')


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


@receiver(user_logged_in)
def user_logged_in_callback(sender, request, user, **kwargs):
    ip = get_client_ip(request)

    logger.info('login user: {user} via ip: {ip}'.format(
        user=user,
        ip=ip
    ))


@receiver(user_logged_out)
def user_logged_out_callback(sender, request, user, **kwargs):
    ip = get_client_ip(request)

    logger.info('logout user: {user} via ip: {ip}'.format(
        user=user,
        ip=ip
    ))


@receiver(user_login_failed)
def user_login_failed_callback(sender, credentials, **kwargs):
    logger.warning('login failed for: {credentials}'.format(
        credentials=credentials,
    ))


class IndexView(generic.ListView):
    """Class for Index view."""

    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions (not including those set to be."""
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')


class DetailView(generic.DetailView):
    """Class Detail for View."""

    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """Excludes any questions that aren't published yet."""
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    """Class for Result in View."""

    model = Question
    template_name = 'polls/results.html'


def index(request):
    """Return function that show index."""
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)


def detail(request, question_id):
    """Return function that show detail."""
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})


def results(request, question_id):
    """Return function that show result."""
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})

@login_required
def vote(request, question_id):
    """Return function that show vote."""
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        messages.success(request, "Your vote is succesfull.")
        if not (question.can_vote()):
            messages.warning(request, "This polls are not allowed.")
        elif Vote.objects.filter(user=request.user, question=question).exists():
            this_votes = Vote.objects.get(user=request.user, question=question)
            this_votes.choice = selected_choice
            this_votes.save()
        else:
            question.vote_set.create(choice=selected_choice, user=request.user)
            messages.success(request,"Vote sucessful,thank you for voting. ")
            logger.info('user {user} voted on polls id: {id}'.format(
                user=request.user,
                id=question_id
            ))
        request.session['choice'] = selected_choice.id
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
