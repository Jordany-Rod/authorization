from datetime import datetime
from lib2to3.fixes.fix_input import context

from django.urls import reverse_lazy

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from unicodedata import category

from .models import Post, Category
from .filters import PostFilter
from .forms import PostForm
from django.contrib.auth.mixins import LoginRequiredMixin
# импортирую PermissionRequiredMixin для предоставления прав доступа
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import login_required

from django.shortcuts import render
from django.shortcuts import get_object_or_404


class PostList(ListView):
    #model = Post
    #ordering = '-title'
    queryset = Post.objects.order_by('-time_in')
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['next_sale'] = 'Распродажа в среду!'
        context['filterset'] = self.filterset
        return context

class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'

# Создание новости
class PostCreateNews(LoginRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit_news.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.art_new = 'NEW'
        return super().form_valid(form)

# Создание статьи
class PostCreateArticles(LoginRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit_articles.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.art_new = 'ART'
        return super().form_valid(form)

# Изменение новости
class PostUpdateNews(LoginRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit_news.html'

# Изменение статьи
class PostUpdateArticles(LoginRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit_articles.html'

# Удаление новости
class PostDeleteNews(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'post_delete_news.html'
    success_url = reverse_lazy('post_list')

# Удаление новости
class PostDeleteArticles(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'post_delete_articles.html'
    success_url = reverse_lazy('post_list')

class MyView(PermissionRequiredMixin, CreateView, UpdateView):
    permission_required = ('news.add_post', 'news.change_post')

class CategoryListView(PostList):
    model = Post
    template_name = 'news/category_list.html'
    context_object_name = 'category_news_list'

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(category=self.category).order_by('-crated_at')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.category.subscribers.all()
        context['category'] = self.category
        return context

@login_required
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)

    massage = 'Вы успешно подписались на рассылку новостей категорий'
    return render(request, 'news/subscribe.html', {'category': category, 'massage': massage})

