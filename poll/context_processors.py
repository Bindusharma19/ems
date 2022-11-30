from .models import Question

def polls_count(request):
    count = Question.objects.count()
    print(count)
    return {"polls_count" : count}