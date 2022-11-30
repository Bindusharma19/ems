from django import forms
from .models import Question, Choice

# My code
class PollForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'status', 'created_by']

#Sir code
class Poll_Form(forms.ModelForm):
    title = forms.CharField(max_length=255, label='Question')

    class Meta:
        model = Question
        fields = ['title',]

class Choice_Form(forms.ModelForm):
    text = forms.CharField(max_length=255, label="Choice")

    class Meta:
        model = Choice
        exclude = ('question',)
