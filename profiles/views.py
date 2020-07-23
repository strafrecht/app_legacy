from django.shortcuts import render
from django.contrib.auth.models import User
from django.shortcuts import redirect
from core.models import Quiz
from wiki.models import ArticleRevision

# Create your views here.
def index(request):
    quizzes = Quiz.objects.filter(user__id=request.user.id).filter(completed=True)
    return render(request, "profiles/index.html", {"quizzes": quizzes})

def quizzes(request):
    quizzes = Quiz.objects.filter(user__id=request.user.id).filter(completed=True).order_by('-created')
    return render(request, "profiles/quizzes.html", {"quizzes": quizzes})

def wiki(request):
    revisions = ArticleRevision.objects.filter(user__id=request.user.id)
    return render(request, "profiles/wiki.html", {"revisions": revisions})

def quiz_summary(request, id):
    quiz = Quiz.objects.get(pk=id)
    return render(request, "profiles/quiz_summary.html", {"quiz": quiz})

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password =  request.POST['password']
        post = User.objects.filter(username=username)
        if post:
            username = request.POST['username']
            request.session['username'] = username
            return redirect("profile:index")
        else:
            return render(request, 'profiles/login.html', {})
    return render(request, 'profiles/login.html', {})

def profile(request):
    if request.session.has_key('username'):
        posts = request.session['username']
        query = User.objects.filter(username=posts)
        return render(request, 'profiles/profile.html', {"query":query})
    else:
        return render(request, 'profiles/login.html', {})

def logout(request):
    try:
        del request.session['username']
    except:
     pass
    return render(request, 'profiles/login.html', {})

