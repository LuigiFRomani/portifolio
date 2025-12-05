from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect

from .models import Post, Comment, Category
from .forms import PostForm, CommentForm

class StaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    login_url = '/accounts/login/'
    raise_exception = True  # se o usuário estiver logado mas sem permissão, retorna 403
    def test_func(self):
        user = getattr(self.request, "user", None)
        return bool(user and (user.is_staff or user.is_superuser))


class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    ordering = ['-posted_at']

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.all()
        context['comment_form'] = CommentForm()
        return context

class PostCreateView(StaffRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

class PostUpdateView(StaffRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

class PostDeleteView(StaffRequiredMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('post_list')
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'
    login_url = '/accounts/login/'  # opcional, por padrão usa settings.LOGIN_URL

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        post_slug = self.kwargs['slug']
        self.object.post = get_object_or_404(Post, slug=post_slug)
        self.object.save()
        return redirect('post_detail', slug=post_slug)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = get_object_or_404(Post, slug=self.kwargs['slug'])
        return context
    
class CategoryListView(ListView):
    model = Category
    template_name = 'blog/category_list.html'
    context_object_name = 'categories'
    ordering = ['name']

class CategoryDetailView(DetailView):
    model = Category
    template_name = 'blog/post_list.html'  # reutiliza o template de listagem de posts
    context_object_name = 'category'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        # let DetailView get the category object into self.object
        context = super().get_context_data(**kwargs)
        category = self.object
        # posts relacionados ordenados do mais recente
        context['posts'] = category.posts.order_by('-posted_at')
        # adiciona a categoria ao contexto (post_list.html espera 'category' quando usado como detail)
        context['category'] = category
        return context