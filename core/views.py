import os
import html2text
import logging
from tqdm import tqdm
import markdownify as md
from bs4 import BeautifulSoup
from collections import deque

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from wiki.models import Article, ArticleRevision, URLPath
from .models import Question, Answer, Quiz, UserAnswer, Choice

logger = logging.getLogger('django')

def index(request):
    #Poll.objects.annotate(choice_count=Count('choice')).filter(choice_count__gt=0)
    #categories = Article.objects.filter(is_category=True)
    #categories = Article.objects.filter(question__isnull=False).filter(is_category=True).filter()
    at = URLPath.objects.get(article=364)
    categories = [child.article for child in at.get_children()]
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

        return render(request, 'core/category_question.html', {'category': category, 'question': question, 'questions': questions})

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
    """
    # init
    path = os.path.abspath("core")
    os.chdir(path)

    # delete all wiki/categories
    URLPath.objects.all().delete()
    ArticleRevision.objects.all().delete()
    Article.objects.all().delete()
    Question.objects.all().delete()

    # Create root article
    root_article = Article(owner=User.objects.first())
    root_article.save()

    urlpath = URLPath(
        slug='stgb',
        article=root_article,
        site_id=1
    )
    urlpath.save()

    root_article.urlpath_set.add(urlpath)
    root_article.save()

    root_article_revision = ArticleRevision(
        article=root_article,
        title="StGB",
        content="links",
        revision_number=1
    )

    root_article_revision.save()

    
    # prepare module
    base_dir = "stgb"
    #get = lambda node_id: Category.objects.get(pk=node_id)
    #root_node = Category.add_root(name="StGB", slug="stgb")

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

                # create categories
                if "category" in get_type(soup):
                    cat = {
                        "root": root,
                        "slug": root.split("/")[-1],
                        "name": soup.article.h1.text.strip(),
                        "long_name": extract("long_name", soup),
                    }

                    create_category(cat)

                # create wikis
                if "problem" in get_type(soup):
                    wiki = {
                        "root": root,
                        "slug": root.split("/")[-1],
                        "name": soup.article.h1.text.strip(),
                        "long_name": extract("long_name", soup),
                        "tags": extract("tags", soup),
                        "content": extract("content", soup),
                    }

                    create_wiki(wiki)

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
    if len(slug_list) == 0:
        return parent
    else:
        remaining = slug_list
        next = remaining.popleft()

        try:
            child = parent.get_children().get(slug=next)
            return traverse_ancestors(child, remaining)
        except URLPath.DoesNotExist:
            return parent
        return parent

def create_category(wiki):
    admin = User.objects.first()
    root = Article.objects.first().urlpath_set.first()

    slug_list = deque(wiki["root"].split("/")[1:])
    parent = traverse_ancestors(root, slug_list)

    # create Article
    article = Article(
        owner=admin,
        is_category=True,
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
        long_name=wiki['long_name'],
        content="LINKS",
        revision_number=1
    )

    # save wiki
    article_revision.save()

    # add tags
    #article_revision.tags.add(*tags)


def create_wiki(wiki):
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
        long_name=wiki['long_name'],
        content=wiki['content'],
        revision_number=1
    )

    # save wiki
    article_revision.save()

    # add tags
    article.tags.add(*tags)

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
        header = soup.article.find(lambda tag: tag.name == "h2" and ("Sachverhalt" in tag.text) or ("Problemaufriss" in tag.text))
        content = ""
        nextNode = header

        while True:
            try:
                tag_name = nextNode.name
            except AttributeError:
                tag_name = "none"

            if tag_name in ["h2","p","ol","li","span", "\n"]:
                # if element has class, remove it
                if 'class' in nextNode.attrs.keys():
                    del nextNode.attrs['class']

                # if child contains class, remove it
                if nextNode.findChild("span"):
                    if 'class' in nextNode.findChild("span").attrs.keys():
                        del nextNode.findChild("span").attrs['class']

                # replace <u> with <b>
                #html = str(nextNode).replace("<u>", " <b>").replace("</u>", "</b> ").replace("<a", " <a").replace("/a>", "/a> ").replace("<span>", "").replace("</span>", "")
                html = str(nextNode).replace("<u>", " <b>").replace("</u>", "</b> ").replace("<span>", "").replace("</span>", "")
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
                long_name=cat["long_name"],
                filepath=cat["root"]
            )
            traverse_category(child, remaining, cat)
            child.save()
"""
