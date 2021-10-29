"""Django views for polls project."""
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Choice, Question, Vote


class IndexView(generic.ListView):
    """Class for index view."""

    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """To Return the last five published questions."""
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')


class DetailView(generic.DetailView):
    """Class for Deatil view."""

    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """Excludes any questions that aren't published yet."""
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    """Class for results view."""

    model = Question
    template_name = 'polls/results.html'

@login_required
def vote(request, question_id):
    """To return vote function."""
    question = get_object_or_404(Question,
                                 pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
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
        return HttpResponseRedirect(reverse('polls:results',args=(question.id,)))
