import os
import json
import html2text
import logging

from django.contrib.auth.decorators import login_required
from rest_framework.permissions import AllowAny
from tqdm import tqdm
from markdownify import markdownify as md
from bs4 import BeautifulSoup
from collections import deque
from time import sleep
from itertools import chain

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.models import User
from django.core import serializers
from wiki.models import Article, ArticleRevision, URLPath
from .models import Question, Answer, Quiz, UserAnswer, Choice
from pages.models import Exams

from rest_framework import viewsets, permissions
from .serializers import QuestionSerializer, ChoiceSerializer, UserAnswerSerializer, QuizSerializer, AnswerSerializer

logger = logging.getLogger('django')

def index(request):
    categories = get_at_categories()
    return render(request, "core/quiz.html", {"categories": categories})

def index_bt(request):
    categories = get_bt_categories()
    return render(request, "core/quiz.html", {"categories": categories})

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'core/question.html', {'question': question})

def category(request, category_id):
    category = get_object_or_404(Article, id=category_id)
    questions = Question.objects.filter(category_id=category_id)
    return render(request, 'core/category.html', {'category': category, 'questions': questions})

def category_question(request, category_id, question_id):
    category = get_object_or_404(Article, id=category_id)

    if request.method == 'POST':
        question_id = request.POST['question-id']

        if request.user:
            question = Question.objects.get(pk=question_id)
            user = User.objects.get(pk=request.user.id)
            quiz = Quiz.objects.filter(category__id=category.id).filter(user__id=user.id).filter(completed=False).last()

            user_answer = UserAnswer(
                question=question,
                quiz=quiz,
            )
            user_answer.save()

            logger.error(request.POST)
            for answer in request.POST.getlist('answer'):
                choice = Choice(
                    user_answer=user_answer,
                    answer=Answer.objects.get(pk=answer)
                )
                choice.save()

            questions = _get_questions_for_category(category_id)

            next_question = questions.filter(id__gt=question_id).first()

            #return render(request, 'core/category_question.html', {'category': category, 'question': next_question, 'questions': questions})
            if request.POST.get('state') == 'finished':
                quiz.completed = True
                quiz.save()

                return HttpResponseRedirect('/profile/quizzes')
            else:
                return HttpResponseRedirect('/quiz/category/{}/question/{}'.format(category.id, next_question.id))
        else:
            request.session['category'][category_id]['question'][question_id]['answer'][answer_id]
    else:
        category = get_object_or_404(Article, id=category_id)

        id = category_id
        # Get article object
        article_schuld = Article.objects.get(pk=id)
        # Get target article's URLPath
        path_schuld = URLPath.objects.get(article=article_schuld.id)
        # Get URLPath descendants
        schuld_descendants = path_schuld.get_descendants()
        # Get Article IDs
        ids = [path.article.id for path in schuld_descendants]
        # Get questions
        questions = Question.objects.filter(category_id=id) | Question.objects.filter(category_id__in=ids)
        question = Question.objects.get(pk=question_id)
        # user
        user = User.objects.get(pk=request.user.id)

        # If user starts a new quiz, create quiz object
        if request.GET.get('state') == 'start':
            quiz = Quiz(
                completed=False,
                category=category,
                user=user,
            )
            quiz.save()

            question = questions.first()

        return render(request, 'core/category_question.html', {
            'category': category,
            'question': question,
            'questions': questions,
            'categories': get_bt_categories() if '/bt' in category.get_absolute_url() else get_at_categories()
        })

def category_summary(request, category_id):
    category = get_object_or_404(Article, id=category_id)
    user_id = request.user.id
    quiz = Quiz.objects.filter(category__id=category.id).filter(user__id=user_id).filter(completed=False).first()
    quiz.completed = True
    quiz.save()

    return render(request, 'core/category_summary.html', {'category': category})

def _get_questions_for_category(category_id):
    id = category_id
    # Get article object
    article_schuld = Article.objects.get(pk=id)
    # Get target article's URLPath
    path_schuld = URLPath.objects.get(article=article_schuld.id)
    # Get URLPath descendants
    schuld_descendants = path_schuld.get_descendants()
    # Get Article IDs
    ids = [path.article.id for path in schuld_descendants]
    # Get questions
    questions = Question.objects.filter(category_id=id) | Question.objects.filter(category_id__in=ids)
    return questions.order_by('id')


def scrape(request):
    # init
    path = os.path.abspath("core")
    os.chdir('/home/admin/Workspace/app/core')

    # delete all wiki/categories
    #URLPath.objects.all().delete()
    #ArticleRevision.objects.all().delete()
    #Article.objects.all().delete()
    Question.objects.all().delete()

    # Create root article
    root_url = URLPath.create_root(title="StGB")
    root_url.save()

    # prepare module
    base_dir = "stgb"
    # get = lambda node_id: Category.objects.get(pk=node_id)
    # root_node = Category.add_root(name="StGB", slug="stgb")

    # preprocess total file count
    # Preprocess the total files count
    filecounter = 0
    for filepath in os.walk(base_dir):
        filecounter += 1

    # run main code
    #for root, dirs, files in os.walk(base_dir, topdown=True, onerror=on_error):
    for root, dirs, files in tqdm(os.walk(base_dir, topdown=True, onerror=on_error), total=filecounter, unit=" files"):

        #if "grundlagen" in root:        
        if True:
            for file in files:
                path = os.path.join(root, file)
                html = open(path).read()
                soup = BeautifulSoup(html, "html.parser")

                print("=> {}".format(path))

                # create categories
                if "category" in get_type(soup):
                    cat = {
                        "root": root,
                        "slug": root.split("/")[-1],
                        "name": soup.article.h1.text.strip(),
                        #"long_name": extract("long_name", soup),
                    }

                    #create_category(cat)

                # create wikis
                if "problem" in get_type(soup):
                    wiki = {
                        "root": root,
                        "slug": root.split("/")[-1],
                        "name": soup.article.h1.text.strip(),
                        #"long_name": extract("long_name", soup),
                        "tags": extract("tags", soup),
                        "content": extract("content", soup),
                    }

                    #create_wiki(wiki)

                # create mct
                if "frage" in get_type(soup):
                    question = {
                        "root": root,
                        "slug": root.split("/")[-1],
                        "category": "", #Category
                        "title": extract("question", soup),
                        "answers": extract("answers", soup),
                        "description": extract("description", soup),
                        "order": extract("order", soup),
                    }

                    create_question(question)

    # output
    #categories = Category.objects.all()
    return render(request, "core/categories.html", {
        "categories": [],
        "wikis": [],
        "questions": [],
    })

def traverse_ancestors(parent, slug_list):
    #print("  ENTER: traverse_ancestors()")
    #print("  parent: {}, slug_list: {}".format(parent, slug_list))

    if len(slug_list) == 0:
        #print("    POS: 1")
        return parent
    else:
        #print("    POS: 2")
        remaining = slug_list
        up = remaining.popleft()
        #print("    UP: {}".format(up))

        try:
            children = parent.get_children()
            child = list(filter(lambda c: c.slug == up, children))

            #print("      CHILDREN: {}".format(child))

            if len(child) == 1:
                #print("        POS: 4")
                return traverse_ancestors(child[0], remaining)
            else:
                raise URLPath.DoesNotExist
        except URLPath.DoesNotExist:
            #print("      POS: 5")
            return parent

        #print("    POS: 6")
        return parent

    #print("  EXIT: traverse_ancestors()")

def old_create_category(wiki):
    admin = User.objects.first()
    root = Article.objects.first().urlpath_set.first()

    slug_list = deque(wiki["root"].split("/")[1:])
    parent = traverse_ancestors(root, slug_list)

    # create Article
    article = Article(
        owner=admin,
        #is_category=True,
    )
    article.save()

    # create URLPath
    urlpath = URLPath(
        parent=parent,
        article=article,
        slug=wiki['slug'],
        site_id=1
    )
    urlpath.save()

    # add URLPath to Article
    article.urlpath_set.add(urlpath)

    article_revision = ArticleRevision(
        article=article,
        title=wiki['name'],
        #long_name=wiki['long_name'],
        content="LINKS",
        revision_number=1
    )

    # save wiki
    article_revision.save()

    # add tags
    #article_revision.tags.add(*tags)

def create_category(wiki):
    #print("ENTER: create_category()")
    root = Article.objects.first().urlpath_set.first()
    slug_list = deque(wiki["root"].split("/")[1:])
    parent = traverse_ancestors(root, slug_list)

    #print("root: {}".format(root))
    #print("slug_list: {}".format(slug_list))
    #print("parent: {}".format(parent))

    urlpath = URLPath.create_urlpath(
        parent=parent,
        slug=wiki['slug'],
        site=None,
        title=wiki['name'],
        article_kwargs={},
        request=None,
        article_w_permissions=None,
        content="",
    )

    urlpath.save()
    #print("EXIT: create_category()")

def create_wiki(wiki):
    #print("ENTER: create_wiki()")
    root = Article.objects.first().urlpath_set.first()
    slug_list = deque(wiki["root"].split("/")[1:])
    parent = traverse_ancestors(root, slug_list)

    #print("root: {}".format(root))
    #print("slug_list: {}".format(slug_list))
    #print("parent: {}".format(parent))

    urlpath = URLPath.create_urlpath(
        parent=parent,
        slug=wiki['slug'],
        site=None,
        title=wiki['name'],
        article_kwargs={},
        request=None,
        article_w_permissions=None,
        content=wiki['content'],
    )

    urlpath.save()

    #print("NEW: {}".format(urlpath))
    #print("EXIT: create_wiki()")

def old_create_wiki(wiki):
    tags = wiki['tags']
    admin = User.objects.first()
    root = Article.objects.first().urlpath_set.first()

    slug_list = deque(wiki["root"].split("/")[1:])
    parent = traverse_ancestors(root, slug_list)

    # create Article
    article = Article(
        owner=admin,
    )
    article.save()

    # create URLPath
    urlpath = URLPath(
        parent=parent,
        article=article,
        slug=wiki['slug'],
        site_id=1
    )
    urlpath.save()

    # add URLPath to Article
    article.urlpath_set.add(urlpath)

    article_revision = ArticleRevision(
        article=article,
        title=wiki['name'],
        #long_name=wiki['long_name'],
        content=wiki['content'],
        revision_number=1
    )

    # save wiki
    article_revision.save()

    # add tags
    # article.tags.add(*tags)

def create_question(question):
    answers = question['answers']

    root = Article.objects.first().urlpath_set.first()
    slug_list = deque(question["root"].split("/")[1:-2])
    parent = traverse_ancestors(root, slug_list)

    question = Question(
        filepath=question['root'],
        slug=question['slug'],
        title=question['title'],
        order=question['order'],
        description=question['description'],
        category=parent.article,
    )

    print(question)

    # save question
    question.save()

    # save answers
    for answer in answers:
        question.answer_set.create(text=answer['text'], correct=answer['correct'])

def get_type(soup):
    return extract("type", soup)

def extract(field, soup):
    if field == "question":
        header = soup.find(lambda tag: tag.name == "h2")
        title = md(header.decode_contents(formatter="html").replace("\n", ""))
        return title

    if field == "answers":
        header = soup.find(lambda tag: tag.name == "h2")
        answers = [{
                'text': md(answer.decode_contents(formatter="html").replace("\n", "")), 
                'correct': 'correct' in answer.attrs.values().__str__()
            } for answer in soup.find("ul").findAll("li")]
        return answers

    if field == "description":
        header = soup.find(lambda tag: tag.name == "ul")
        html = "<br>".join([str(p) for p in header.findNextSiblings("p")])
        markdown = md(html)
        description = markdown
        return description

    # [Wiki]
    if field == "tags":
        header = soup.find(lambda tag: tag.name == "h2" and "Tags" in tag.text)

        try:
            tag_list = header.findNextSibling("p").text.replace("\n", "").replace("§", " §").split(";")
            tag_list = [tag.strip() for tag in tag_list]
        except AttributeError:
            tag_list = []
        return tag_list

    #
    if field == "content":
        header = soup.article.find(lambda tag: tag.name == "h2" and ("Sachverhalt" in tag.text) or ("Problemaufriss" in tag.text) or ("Tags" in tag.text))
        if "siehe hier" in soup.prettify():
            nextNode = soup.article.find("p")
        else:
            nextNode = header
        content = ""

        while True:
            try:
                tag_name = nextNode.name
            except AttributeError:
                tag_name = "none"

            if tag_name in ["h2","p","ol","li","span", "\n", "h5"]:
                # if element has class, remove it
                if 'class' in nextNode.attrs.keys():
                    del nextNode.attrs['class']

                # if child contains class, remove it
                if nextNode.findChild("span"):
                    if 'class' in nextNode.findChild("span").attrs.keys():
                        del nextNode.findChild("span").attrs['class']

                # replace <u> with <b>
                #html = str(nextNode).replace("<u>", " <b>").replace("</u>", "</b> ").replace("<a", " <a").replace("/a>", "/a> ").replace("<span>", "").replace("</span>", "")
                html = str(nextNode).replace("<u>", " <b>").replace("</u>", "</b> ").replace("<span>", "").replace("</span>", "").replace("<em>", "<i>").replace("</em>", "</i>").replace("<h5", "<p").replace("</h5>", "</p>")

                if "Fragment" in html: html = html.replace("<!--StartFragment-->", "").replace("<!--EndFragment-->", "")
                if "siehe hier" in soup.prettify():
                    html = html.replace("problemfelder", "wiki")
                markdown = md(html)
                content += markdown
            elif tag_name == "sonline-revision":
                break
            else:
                False

            try:
                nextNode = nextNode.nextSibling
            except AttributeError:
                break

        return content

    if field == "order":
        value = soup.article.attrs["data-order"]

        # if order is datetime value, return order 1000
        try:
            return value
        except:
            return "6666"

    if field == "long_name":
        return soup.article.attrs["data-short-name"]
    if field == "type":
        return soup.article.attrs["data-type"].split("/")[-1]

def on_error(e):
    raise e

#def match_category(root):
#    list = root.split("/")[:-1]
#    filepath = "/".join(list)
#
#    try:
#        category = Category.objects.filter(filepath=filepath).first()
#        return category
#    except AttributeError:
#        return None

def _create_category(node, cat):
    # 
    remaining = deque(cat["root"].split("/")[1:])
    traverse_category(node, remaining, cat)

def _traverse_category(node, remaining, cat):
    # if any items remain in path list, keep traversing
    if remaining:
        current = remaining.popleft()

        if node.get_children().filter(slug=current):
            child = node.get_children().get(slug=current)
            traverse_category(child, remaining, cat)
        else:
            child = node.add_child(
                name=cat["name"],
                slug=cat["slug"],
                #long_name=cat["long_name"],
                filepath=cat["root"]
            )
            traverse_category(child, remaining, cat)
            child.save()

def exams(request):
    import csv
    import dateutil.parser

    exams = []

    with open('exams.csv', newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        exam_type = {
            'Klausur im Falltraining': 'falltraining',
            'Examensklausur': 'exam',
            'Originalexamensklausur': 'original-exam',
            'Übungsfall': 'exercise',
            'Übungsklausur': 'exercise',
            'AG-Fall': 'tutorial',
        }
        exam_difficulty = {
            'Anfänger': 'beginner',
            'Fortgeschrittene': 'intermediate',
            'Examen': 'advanced',
        }

        for row in reader:
            if row[0]:
                date_string = "{}-01".format(row[0])
                print(repr(date_string))
                date = dateutil.parser.parse(date_string)
            else:
                date = None

            if row[1]:
                et = exam_type[row[1]]
            else:
                et = ""

            if row[2]:
                ed = exam_difficulty[row[2]]
            else:
                ed = ""

            exam = Exams.objects.create(
                date=date,
                type=et,
                difficulty=ed,
                paragraphs=row[3],
                problems=row[4],
                sachverhalt_link=row[5],
                loesung_link=row[6],
            )
            
            exams.append(exam)

    for exam in exams: print(exam)

    result = Exams.objects.bulk_create(exams)

    if result:
        return HttpResponse('<p>done</p>')
    else:
        return HttpResponse('<p>failed</p>')


def search_wiki(request, query = False):
    from django.contrib.postgres.search import SearchVector, TrigramSimilarity, TrigramDistance
    #articles = Article.objects.annotate(
    #    #similarity=TrigramSimilarity('current_revision__title', query),
    #    distance=TrigramDistance('current_revision__content', query),
    #).filter(distance__gt=0.7).order_by('distance')

    if query:
        results = Article.objects.annotate(
            search=SearchVector(
            #'current_revision__title',
            'current_revision__content',
            ),
        ).filter(search__icontains=query)
    else:
        results = Article.objects.all()

    articles = [{
        'title': article.current_revision.title,
        'url': article.get_absolute_url(),
        'content': article.current_revision.content,
        #'breadcrumb': " / ".join([ancestor.article.current_revision.title for ancestor in article.ancestor_objects()])
    } for article in results if sum(1 for x in article.get_children()) == 0 and article.id != 1]

    # get breadcrumb
    # filter by content

    return JsonResponse({'data': articles})

def api_exams(request):
    exams = Exams.objects.all()

    data = [{
    	'id': exam.id,
    	'type': exam.type,
    	'datetime': exam.date,
    	'difficulty': exam.difficulty,
    	'paragraphs': exam.paragraphs,
    	'problems': exam.problems,
    	'situation': exam.sachverhalt_link,
    	'solution': exam.loesung_link,
    } for exam in exams]

    return JsonResponse({'data': data})

def get_first_at(cat):
    categories = [child for child in cat.get_descendants()]
    question_set = [sub.article.question_set.all() for sub in categories if len(sub.article.question_set.all()) > 0]
    pre = [[q for q in question] for question in question_set]
    result = list(chain.from_iterable(pre))
    if len(result) > 0:
        return result[0]
    else:
        Question.objects.first()

def get_first_bt(cat):
    cur_question_set = cat.article.question_set.all()
    question_set = [sub.article.question_set.all() for sub in cat.get_descendants() if len(sub.article.question_set.all()) > 0]

    pre = [[q for q in question] for question in question_set]
    result = list(chain.from_iterable(pre)) + [question for question in list(cur_question_set)]

    if len(result) > 0:
        return result[0]
    else:
        #print("YYY")
        Question.objects.first()

def get_at_categories():
    at = URLPath.objects.filter(slug='at').last()
    grundlagen = URLPath.objects.filter(slug='grundlagen').first()

    categories = [
        {"category": child,
        "first": get_first_at(child),
        "questions": [
            [
                question for question in sub.article.question_set.all() if len(sub.article.question_set.all()) > 1
            ] for sub in child.get_descendants() if len(child.get_descendants()) > 0
        ]} for child in at.get_children()]

    categories.insert(0, {
        "category": grundlagen,
        "first": grundlagen.article.question_set.first(),
        "questions": [
            question for question in grundlagen.article.question_set.all() if len(grundlagen.article.question_set.all()) > 1
        ]
    })

    return categories

def get_bt_categories():
    bt = URLPath.objects.filter(slug='bt').first()

    categories = [
        {"category": child,
        "first": get_first_bt(child),
        "questions": [
            [
            question for question in child.article.question_set.all() if len(child.article.question_set.all()) > 0
        ]
    ]} for child in bt.get_children()]

    categories.sort(key=lambda c: c["category"].path)

    return categories


@login_required(login_url="/profile/login")
def add_question(request):
    return render(request, 'core/add_question.html', {})


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [AllowAny]


class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [AllowAny]


class QuizViewSet(viewsets.ModelViewSet):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = [AllowAny]


class UserAnswerViewSet(viewsets.ModelViewSet):
    queryset = UserAnswer.objects.all()
    serializer_class = UserAnswerSerializer
    permission_classes = [AllowAny]


class ChoiceViewSet(viewsets.ModelViewSet):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer
    permission_classes = [AllowAny]
