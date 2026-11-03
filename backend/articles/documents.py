from django_elasticsearch_dsl import Document, Index, fields

from articles.models import Article, Tag


articles_index = Index("articles")
articles_index.settings(number_of_shards=1, number_of_replicas=0)


@articles_index.document
class ArticleDocument(Document):
    author = fields.ObjectField(
        properties={
            "username": fields.KeywordField(),
        }
    )
    tags = fields.KeywordField(multi=True)

    class Django:
        model = Article
        fields = [
            "title",
            "slug",
            "description",
            "body",
        ]
        related_models = [Tag]

    def prepare_author(self, instance):
        return {"username": instance.author.username}

    def prepare_tags(self, instance):
        return list(instance.tag_list.values_list("name", flat=True))

    def get_instances_from_related(self, related_instance):
        if isinstance(related_instance, Tag):
            return related_instance.articles.all()
        return []
