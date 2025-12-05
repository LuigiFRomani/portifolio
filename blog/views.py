from django.shortcuts import render, redirect, get_object_or_404
from .models import Post
from django.utils import timezone

def post_list(request):
    posts = Post.objects.order_by('-posted_at')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

def post_create(request):
    if request.method == 'POST':
        title = request.POST.get('title','')
        content = request.POST.get('content','')
        post = Post.objects.create(title=title, content=content, posted_at=timezone.now())
        return redirect('post_detail', pk=post.pk)
    return render(request, 'blog/post_form.html', {'action': 'create'})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        post.title = request.POST.get('title','')
        post.content = request.POST.get('content','')
        post.save()
        return redirect('post_detail', pk=post.pk)
    return render(request, 'blog/post_form.html', {'post': post, 'action': 'edit'})

def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        post.delete()
        return redirect('post_list')
    return render(request, 'blog/post_confirm_delete.html', {'post': post})