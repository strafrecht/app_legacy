from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from treebeard.mp_tree import MP_Node
from taggit.managers import TaggableManager
from wiki.models import Article, ArticleRevision, URLPath
import logging

logger = logging.getLogger('django')

class Question(models.Model):
    filepath = models.CharField(max_length=255, null=True, blank=True)
    slug = models.CharField(max_length=255, null=True, blank=True)
    order = models.CharField(max_length=255, null=True, blank=True)
    category = models.ForeignKey('wiki.Article', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        #return self.questionversion_set.all().first().title
        return "{}".format(self.id)

class QuestionVersion(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    slug = models.CharField(max_length=255, blank=True, null=True)
    title = models.TextField(max_length=255)
    description = models.TextField(null=True, blank=True)
    # category = models.ForeignKey('wiki.Article', on_delete=models.SET_NULL, null=True, blank=True)
    categories = models.ManyToManyField(Article, null=True, blank=True)
    approved = models.BooleanField(default=False)

#class Answer(models.Model):
#    question = models.ForeignKey(Question, on_delete=models.CASCADE)
#    text = models.TextField()
#    correct = models.BooleanField(default=False)
#
#    def __str__(self):
#        return self.text

class AnswerVersion(models.Model):
    question_version = models.ForeignKey(QuestionVersion, on_delete=models.CASCADE)
    text = models.TextField()
    correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text

class Quiz(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    category = models.ForeignKey('wiki.Article', on_delete=models.SET_NULL, null=True, blank=True)
    completed = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def calculate_score(self):
        if self.useranswer_set:
            user_answers = self.useranswer_set.all()
            x = {}
            y = {}

            total = 0

            for user_answer in user_answers:
                answers = set()
                uanswers = set()

                if hasattr(y, 'question'):

                    for answer in user_answer.question.answer_set.all():
                        if answer.correct:
                            answers.add(answer.id)

                    for choice in user_answer.choice_set.all():
                        uanswers.add(choice.answer.id)

                    # real answers
                    x[user_answer.question.id] = answers
                    # user answers
                    y[user_answer.question.id] = uanswers

                    if y[user_answer.question.id] == x[user_answer.question.id]:
                        total += 1

            return total

    def total_questions(self):
        return self._get_questions_for_category().count()

    def _get_questions_for_category(self):
        id = self.category.id
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



class UserAnswer(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, null=True, on_delete=models.SET_NULL)
    answer = models.ForeignKey(AnswerVersion, null=True, on_delete=models.SET_NULL)
    created = models.DateTimeField(auto_now_add=True)

class Choice(models.Model):
    user_answer = models.ForeignKey(UserAnswer, null=True, on_delete=models.SET_NULL)
    answer = models.ForeignKey(AnswerVersion, null=True, on_delete=models.SET_NULL)
