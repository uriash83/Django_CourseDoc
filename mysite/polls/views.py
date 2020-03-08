from .models import Choice, Question
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from .models import Choice, Question


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    # domyslny template_name to : <app name>/<model name>_list.html

    # dla ListView mamy dostęp do listy dzięki model poprzez question_list
    # ale można to override poprzez context_object_name

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'
    # for DetailView thanks to model mamy dostęp do Question poprzez question

    # domyslny template to <app name>/<model name>_detail.html polls/question_detail
    # my tego nid używamy gdyż mamy zdefiniowany templat_name


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


# def index(request):


#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     context = {'latest_question_list': latest_question_list}
#     return render(request, 'polls/index.html', context)

# def detail(request, question_idd):
#     question = get_object_or_404(Question, pk=question_idd)
#     return render(request, 'polls/detail.html', {'question': question})
#     #poniższy i powyższy 404 zwraca taki sam błąd 404
#     #try:
#     #    question = Question.objects.get(pk=question_idd)
#     #except Question.DoesNotExist:
#     #   raise Http404("Question does not exist")
#     #return render(request, 'polls/detail.html', {'question': question})

# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/results.html', {'question': question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
        # request.POST['choice'] - zwraca id z choice, strings
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
