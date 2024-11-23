from django.shortcuts import get_object_or_404, render
from django.http import Http404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.views import generic
from .models import Choice, Question

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

# Here is flaw number 2:
# Broken authentication
def vote(request, question_id):
    with connection.cursor() as cursor:
        # Here is flaw number 1:

        cursor.execute(f"SELECT * FROM polls_question WHERE id = {question_id}")
        question = cursor.fetchone()
    if not question:
        raise Http404("Question does not exist")