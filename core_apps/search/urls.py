"""
Search app urls.
"""
from django.urls import path
from .views import ArticleElasticSearchView

urlspatterns = [
    path(
        "search/",
        ArticleElasticSearchView.as_view({"get": "list"}),
        name="article_search",
    ),
]