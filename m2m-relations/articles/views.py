from django.shortcuts import render
from articles.models import Article, ArticleScope


def articles_list(request):
    template = 'articles/news.html'

    articles = Article.objects.all()
    relation_list = ArticleScope.objects.select_related('article', 'scope').order_by('article', '-is_main', 'scope')
    context = {"object_list": articles, "relation_list": relation_list}

    return render(request, template, context)

