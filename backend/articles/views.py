from rest_framework.decorators import action
from rest_framework.mixins import (
    RetrieveModelMixin,
    DestroyModelMixin,
    ListModelMixin,
)
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from django.db.models import Case, IntegerField, When
from elasticsearch import ConnectionError as ElasticsearchConnectionError
from rest_framework.exceptions import APIException

from articles.filters import ArticleFilter
from articles.documents import ArticleDocument
from articles.models import Article, Tag, Comment
from articles.paginations import ArticlePagination
from articles.serializers import ArticleSerializer, CommentSerializer
from utils import mixins


class ArticleViewSet(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    DestroyModelMixin,
    GenericViewSet,
):
    object_name = "article"
    lookup_field = "slug"
    lookup_url_kwarg = "slug"
    serializer_class = ArticleSerializer
    pagination_class = ArticlePagination
    filterset_class = ArticleFilter

    def get_queryset(self):
        queryset = (
            Article.objects.select_related("author")
            .prefetch_related("tag_list", "favored_by")
            .all()
            .order_by("-created_at")
        )
        if self.action in ["update", "destroy"]:
            return queryset.filter(author=self.request.user)
        if self.action == "feed":
            queryset = queryset.filter(author__followers=self.request.user)

        search_term = self.request.query_params.get("search", "").strip()
        if search_term:
            try:
                article_ids = [
                    hit.meta.id
                    for hit in ArticleDocument.search()
                    .query(
                        "multi_match",
                        query=search_term,
                        fields=[
                            "title^3",
                            "description^2",
                            "body",
                            "author.username",
                            "tags",
                        ],
                    )
                    .source(False)
                ]
            except ElasticsearchConnectionError as exc:
                raise APIException(
                    "Article search is temporarily unavailable."
                ) from exc

            if not article_ids:
                return queryset.none()

            queryset = queryset.filter(pk__in=article_ids).annotate(
                search_order=Case(
                    *[
                        When(pk=article_id, then=position)
                        for position, article_id in enumerate(article_ids)
                    ],
                    output_field=IntegerField(),
                )
            ).order_by("search_order")

        return queryset

    def get_permissions(self):
        if self.request.method not in SAFE_METHODS or self.action == "feed":
            return [IsAuthenticated()]
        return []

    @action(detail=False)
    def feed(self, request, *args, **kwargs):
        return self.list(self, request, *args, **kwargs)

    @action(detail=True, methods=["POST", "DELETE"])
    def favorite(self, request, *args, **kwargs):
        article = self.get_object()
        if request.method == "POST":
            article.favored_by.add(request.user)
        else:
            article.favored_by.remove(request.user)
        return Response(self.get_serializer(article).data)


class TagListView(APIView):
    @staticmethod
    def get(request):
        return Response({"tags": Tag.objects.popular_tags()})


class CommentViewSet(
    mixins.CreateModelMixin, ListModelMixin, DestroyModelMixin, GenericViewSet
):
    object_name = "comment"
    serializer_class = CommentSerializer

    def get_permissions(self):
        if self.action in ["create", "destroy"]:
            return [IsAuthenticated()]
        return []

    def get_queryset(self):
        queryset = (
            Comment.objects.select_related("author")
            .filter(article__slug=self.kwargs["article_slug"])
            .order_by("-created_at")
        )
        if self.action == "destroy":
            return queryset.filter(author=self.request.user)
        return queryset

    def perform_create(self, serializer):
        article = Article.objects.get(slug=self.kwargs["article_slug"])
        serializer.save(author=self.request.user, article=article)
