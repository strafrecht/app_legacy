from core.models import *
from rest_framework import serializers


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        # fields = "__all__"
        fields = ['id', 'filepath', 'slug', 'title', 'order', 'description', 'category']


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerVersion
        # fields = "__all__"
        fields = ['id', 'question', 'text', 'correct']


class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        # fields = "__all__"
        fields = ['id', 'user', 'category', 'completed', 'created', 'updated']


class UserAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAnswer
        # fields = "__all__"
        fields = ['id', 'quiz', 'question', 'created']


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        # fields = "__all__"
        fields = ['id', 'user_answer', 'answer']
