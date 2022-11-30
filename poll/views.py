from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from .models import Question, Choice, Answer
from ems.decorators import role_required
from django.contrib.auth.decorators import login_required
from .forms import PollForm, Poll_Form, Choice_Form
from ems.decorators import hr_only
from django.views.generic import View
from django.utils.decorators import method_decorator

# Create your views here.

class PollView(View):
    decorators = [login_required, hr_only]

    @method_decorator(decorators)
    def get(self, request, id=None):
        if id:
            question = get_object_or_404(Question, id=id)
            choices = question.choice_set.all()
            poll_form = Poll_Form(instance=question)
            choice_forms = [Choice_Form(prefix=str(choice.id), instance=choice) for choice in choices]
            template = 'poll/edit_poll.html'
        else:
            poll_form = Poll_Form(instance=Question())
            choice_forms = [Choice_Form(prefix=str(x), instance=Choice()) for x in range(3)]
            template = 'poll/new_poll.html'
        context = {
            'poll_form' : poll_form,
            'choice_forms' : choice_forms,
        }
        return render(request, template, context)

    @method_decorator(decorators)
    def post(self, request, id=None):
        context = {}
        if id:
            self.put(request, id)
        poll_form = Poll_Form(request.POST, instance=Question())
        choice_forms = [Choice_Form(request.POST, prefix=str(x), instance=Choice()) for x in range(0, 3)]
        if poll_form.is_valid and all([cf.is_valid() for cf in choice_forms]):
            new_poll = poll_form.save(commit=False)
            new_poll.created_by = request.user
            new_poll.save()
            for cf in choice_forms:
                new_choice = cf.save(commit=False)
                new_choice.question = new_poll
                new_choice.save()
            return HttpResponseRedirect(reverse('polls_list'))
        context = {'poll_form': poll_form, 'choice_forms' : choice_forms,}
        return render(request, 'poll/new_poll.html', context)

    @method_decorator(decorators)
    def put(self, request, id=None):
        context = {}
        question = get_object_or_404(Question, id=id)
        poll_form = Poll_Form(request.POST, instance=question)
        choice_forms = [Choice_Form(request.POST, prefix=str(
            choice.id), instance=choice) for choice in question.choice_set.all()]
        if poll_form.is_valid and all([cf.is_valid for cf in choice_forms]):
            new_poll = poll_form.save(commit=False)
            new_poll.created_by = request.user
            new_poll.save()
            for cf in choice_forms:
                new_choice = cf.save(commit=False)
                new_choice.question = new_poll
                new_choice.save()
            return redirect('polls_list')
        context = {'poll_form' : poll_form, 'choice_forms' : choice_forms,}
        return render(request, 'poll/edit_poll.html', context)


@login_required(login_url="/login/")
def index(request):
    questions = Question.objects.all().order_by('-created_at')

    context = {
        'title' : 'polls',
        'questions' : questions,
    }
    return render(request, 'poll/index.html', context)

@login_required(login_url="/login/")
def details(request, id):
    try:
        question = Question.objects.get(pk=id)
        #choices = question.choice_set.all()
    except:
        raise Http404
    context = {
        'question' : question,

    }
    return render(request, 'poll/details.html', context)

@login_required(login_url="/login/")
def poll(request, id):
    if request.method == "GET":
        try:
            question = Question.objects.get(id=id)
        except:
            raise Http404
        context = {
            'question' : question,
        }
        return render(request, 'poll/poll.html', context)
    if request.method == "POST":
        user_id = 1
        data = request.POST.get('choice')
        print(data)
        ret = Answer.objects.create(user_id=user_id, choice_id=data)
        if ret:
            return HttpResponse(f"Your voting is done successfully")
        else:
            return HttpResponse(f"Your voting is done successfully")

@role_required(allowed_roles=['HR'])
def add_poll(request):
    if request.method == "POST":
        poll_form = PollForm(request.POST)
        context = {
            'poll_form' : poll_form,
        }
        if poll_form.is_valid():
            poll_form.save()
            return HttpResponseRedirect(reverse('polls_list'))
        else:
            return render(request, 'poll/add_poll.html', context)
    else:
        poll_form = PollForm()
        context = {
            'poll_form': poll_form,
        }
        return render(request, 'poll/add_poll.html', context)

@login_required(login_url='/login/')
@role_required(allowed_roles=['HR'])
def add_choice(request):
    if request.method == "GET":
        questions = Question.objects.all()
        context = {
            'questions' : questions,
        }
        return render(request, 'poll/add_choice.html', context)
    if request.method == "POST":
        q_id = request.POST.get('select_question')
        question = Question.objects.get(id=q_id)
        choice = question.choice_set.create(text=request.POST.get('text'))
        choice.save()
        print(question)
        print(choice)
        return HttpResponseRedirect(reverse('polls_list'))


















