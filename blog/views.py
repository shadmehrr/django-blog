from django.views.generic import ListView, DetailView
from account.models import User
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from account.mixins import AuthorAccessMixin
# from django.http import HttpResponse, JsonResponse, Http404
from .models import Article, Category
from django.db.models import Q

# Create your views here.
class ArticleList(ListView):
	queryset = Article.objects.published()
	paginate_by = 5


class ArticleDetail(DetailView):
	def get_object(self):
		slug = self.kwargs.get('slug')
		return get_object_or_404(Article.objects.published(), slug=slug)


class ArticlePreview(AuthorAccessMixin, DetailView):
	def get_object(self):
		pk = self.kwargs.get('pk')
		return get_object_or_404(Article, pk=pk)


class CategoryList(ListView):
	paginate_by = 5
	template_name = 'blog/category_list.html'

	def get_queryset(self):
		global category
		slug = self.kwargs.get('slug')
		category = get_object_or_404(Category.objects.active(), slug=slug)
		return category.articles.published()

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['category'] = category
		return context


class AuthorList(ListView):
	paginate_by = 5
	template_name = 'blog/author_list.html'

	def get_queryset(self):
		global author
		username = self.kwargs.get('username')
		author = get_object_or_404(User, username=username)
		return author.articles.published()

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['author'] = author
		return context



class SearchList(ListView):
	paginate_by = 5
	template_name = 'blog/search_list.html'

	def get_queryset(self):
		search = self.request.GET.get('q')
		return Article.objects.filter(Q(description__icontains=search) | Q(title__icontains=search))

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['search'] = self.request.GET.get('q')
		return context