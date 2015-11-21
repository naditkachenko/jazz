from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post, Comment
from .forms import CommentForm

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts':posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method=='POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.created_date = timezone.now()
            comment.save()
            return redirect('post_detail', pk=post.id)
    else:
        form = CommentForm()
    comments = Comment.objects.filter(post=post).order_by('-created_date')
    return render(request, 'blog/post_detail.html', {'post': post,
                                                     'form':form,
                                                     'comments':comments})

