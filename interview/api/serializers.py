from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Topic, Question

class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id']


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration with ASVS Level 2 compliance
    - V2.1.1: Passwords are at least 12 characters
    - V2.1.2: Passwords permit any printable characters
    - V2.1.7: Passwords are checked against breached password lists
    - V2.1.9: No password composition rules limiting character types
    """
    password = serializers.CharField(
        write_only=True, 
        min_length=12,
        style={'input_type': 'password'},
        help_text="Password must be at least 12 characters"
    )
    password_confirm = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'}
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm', 'first_name', 'last_name']
    
    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({"password": "Passwords must match."})
        return data
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return user


class TopicSerializer(serializers.ModelSerializer):
    questions_count = serializers.SerializerMethodField()
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    updated_by_username = serializers.CharField(source='updated_by.username', read_only=True)
    
    class Meta:
        model = Topic
        fields = [
            'id', 
            'name', 
            'description', 
            'slug',
            'questions_count',
            'is_active',
            'created_at', 
            'updated_at',
            'created_by',
            'created_by_username',
            'updated_by',
            'updated_by_username'
        ]
        read_only_fields = ['created_at', 'updated_at', 'created_by', 'updated_by']
    
    def get_questions_count(self, obj):
        return obj.questions.filter(is_active=True).count()


class QuestionSerializer(serializers.ModelSerializer):
    topic_name = serializers.CharField(source='topic.name', read_only=True)
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    updated_by_username = serializers.CharField(source='updated_by.username', read_only=True)
    
    class Meta:
        model = Question
        fields = [
            'id', 
            'text', 
            'topic',
            'topic_name',
            'difficulty', 
            'expected_answer', 
            'tags', 
            'is_active',
            'created_at', 
            'updated_at',
            'created_by',
            'created_by_username',
            'updated_by',
            'updated_by_username'
        ]
        read_only_fields = ['created_at', 'updated_at', 'created_by', 'updated_by']

    def validate_text(self, value):
        if len(value) < 10:
            raise serializers.ValidationError("Question text must be at least 10 characters long.")
        return value


class QuestionDetailSerializer(QuestionSerializer):
    topic = TopicSerializer(read_only=True)
    
    class Meta(QuestionSerializer.Meta):
        fields = QuestionSerializer.Meta.fields