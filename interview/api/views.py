from rest_framework import viewsets, filters, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
    AllowAny,
    IsAuthenticated,
)
from django.contrib.auth.models import User
from .models import Topic, Question
from .serializers import (
    TopicSerializer,
    QuestionSerializer,
    QuestionDetailSerializer,
    UserSerializer,
    UserRegistrationSerializer,
)
from rest_framework.views import APIView
from rest_framework.response import Response


class VersionAPIView(APIView):
    permission_classes = [AllowAny]  # optional

    def get(self, request):
        return Response({"version": "1.0.0"})


class UserRegistrationView(generics.CreateAPIView):
    """
    API endpoint for user registration
    """

    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]


class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    API endpoint for viewing and updating user profile
    """

    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class TopicViewSet(viewsets.ModelViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name", "description"]
    ordering_fields = ["name", "created_at"]
    lookup_field = "slug"

    def get_queryset(self):
        queryset = Topic.objects.all()

        # Filter by active status
        is_active = self.request.query_params.get("is_active")
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == "true")

        return queryset

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

    @action(detail=True, methods=["get"])
    def questions(self, request, slug=None):
        """Get all questions for a specific topic"""
        topic = self.get_object()
        questions = topic.questions.filter(is_active=True)

        # Apply difficulty filter if provided
        difficulty = request.query_params.get("difficulty")
        if difficulty:
            questions = questions.filter(difficulty=difficulty)

        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.select_related(
        "topic", "created_by", "updated_by"
    ).all()
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["text", "tags", "topic__name"]
    ordering_fields = ["created_at", "difficulty", "topic__name"]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return QuestionDetailSerializer
        return QuestionSerializer

    def get_queryset(self):
        queryset = Question.objects.select_related(
            "topic", "created_by", "updated_by"
        ).all()

        # Filter by topic
        topic = self.request.query_params.get("topic")
        if topic:
            queryset = queryset.filter(topic__slug=topic)

        # Filter by difficulty
        difficulty = self.request.query_params.get("difficulty")
        if difficulty:
            queryset = queryset.filter(difficulty=difficulty)

        # Filter by active status
        is_active = self.request.query_params.get("is_active")
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == "true")

        return queryset

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

    @action(detail=False, methods=["get"])
    def random(self, request):
        """Get a random question"""
        queryset = self.get_queryset().filter(is_active=True)

        # Apply filters
        topic = request.query_params.get("topic")
        if topic:
            queryset = queryset.filter(topic__slug=topic)

        difficulty = request.query_params.get("difficulty")
        if difficulty:
            queryset = queryset.filter(difficulty=difficulty)

        question = queryset.order_by("?").first()
        if question:
            serializer = self.get_serializer(question)
            return Response(serializer.data)
        return Response({"detail": "No questions available"}, status=404)

    @action(detail=False, methods=["get"])
    def by_topic(self, request):
        """Get questions grouped by topic"""
        topics = Topic.objects.filter(is_active=True)
        result = {}
        for topic in topics:
            questions = Question.objects.filter(topic=topic, is_active=True)
            result[topic.name] = QuestionSerializer(questions, many=True).data
        return Response(result)

    @action(detail=False, methods=["get"])
    def statistics(self, request):
        """Get statistics about questions"""
        total_questions = Question.objects.filter(is_active=True).count()
        by_difficulty = {}
        for difficulty, _ in Question.DIFFICULTY_CHOICES:
            count = Question.objects.filter(
                difficulty=difficulty, is_active=True
            ).count()
            by_difficulty[difficulty] = count

        by_topic = {}
        topics = Topic.objects.filter(is_active=True)
        for topic in topics:
            count = Question.objects.filter(topic=topic, is_active=True).count()
            by_topic[topic.name] = count

        return Response(
            {
                "total_questions": total_questions,
                "by_difficulty": by_difficulty,
                "by_topic": by_topic,
            }
        )

    @action(detail=False, methods=["get"], permission_classes=[IsAuthenticated])
    def my_questions(self, request):
        """Get questions created by the current user"""
        questions = Question.objects.filter(created_by=request.user)
        serializer = self.get_serializer(questions, many=True)
        return Response(serializer.data)
