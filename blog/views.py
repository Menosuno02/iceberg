import random
from itertools import chain

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.template.loader import render_to_string
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from blog.utils import is_ajax
from notification.models import Notification
from users.models import Profile

from .forms import CommentForm
from .models import Comment, Post

""" Página inicio con posts """
def first(request):
    return render(request, 'blog/first.html', {'posts':Post.objects.all()})

""" Posts de usuarios seguidos """
@login_required
def posts_of_following_profiles(request):
    profile = Profile.objects.get(user = request.user)
    users = [user for user in profile.following.all()]
    posts = []
    qs = None
    for u in users:
        p = Profile.objects.get(user=u)
        p_posts = p.user.post_set.all()
        posts.append(p_posts)
    my_posts = profile.profile_posts()
    posts.append(my_posts)
    if len(posts)>0:
        qs = sorted(chain(*posts), reverse=True, key=lambda obj:obj.date_posted)

    paginator = Paginator(qs, 5)
    page = request.GET.get('page')
    try:
        posts_list = paginator.page(page)
    except PageNotAnInteger:
        posts_list = paginator.page(1)
    except EmptyPage:
        posts_list = paginator.page(paginator.num_pages)

    return render(request,'blog/feeds.html',{'profile':profile,'posts':posts_list})


""" Me gusta a post """
@login_required
def LikeView(request):
    post = get_object_or_404(Post, id=request.POST.get('id'))
    liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
        notify = Notification.objects.filter(post=post, sender=request.user, notification_type=1)
        notify.delete()
    else:
        post.likes.add(request.user)
        liked = True
        notify = Notification(post=post, sender=request.user, user=post.author, notification_type=1)
        notify.save()
    context = {
        'post':post,
        'total_likes':post.total_likes(),
        'liked':liked,
    }
    if is_ajax(request=request):
        html = render_to_string('blog/like_section.html',context, request=request)
        return JsonResponse({'form':html})


""" Guardar post """
@login_required
def SaveView(request):
    post = get_object_or_404(Post, id=request.POST.get('id'))
    saved = False
    if post.saves.filter(id=request.user.id).exists():
        post.saves.remove(request.user)
        saved = False
    else:
        post.saves.add(request.user)
        saved = True
    context = {
        'post':post,
        'total_saves':post.total_saves(),
        'saved':saved,
    }
    if is_ajax(request=request):
        html = render_to_string('blog/save_section.html',context, request=request)
        return JsonResponse({'form':html})


""" Me gusta comentario de post """
@login_required
def LikeCommentView(request):
    post = get_object_or_404(Comment, id=request.POST.get('id'))
    cliked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        cliked = False
    else:
        post.likes.add(request.user)
        cliked = True

    cpost = get_object_or_404(Post, id=request.POST.get('pid'))
    total_comments2 = cpost.comments.all().order_by('-id')
    total_comments = cpost.comments.all().filter(reply=None).order_by('-id')
    tcl={}
    for cmt in total_comments2:
        total_clikes = cmt.total_clikes()
        cliked = False
        if cmt.likes.filter(id=request.user.id).exists():
            cliked = True

        tcl[cmt.id] = cliked

    context = {
        'comment_form':CommentForm(),
        'post':cpost,
        'comments':total_comments,
        'total_clikes':post.total_clikes(),
        'clikes':tcl
    }

    if is_ajax(request=request):
        html = render_to_string('blog/comments.html',context, request=request)
        return JsonResponse({'form':html})


""" Página de inicio con los posts """
class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html' 
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

    def get_context_data(self, *args,**kwargs):
        context = super(PostListView, self).get_context_data()
        users = list(User.objects.exclude(pk=self.request.user.pk))
        if len(users) > 3:
            cnt = 3
        else:
            cnt = len(users)
        random_users = random.sample(users, cnt)
        context['random_users'] = random_users
        return context


""" Todos los posts del usuario """
class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html' 
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


""" Post detallado """
def PostDetailView(request,pk):
    stuff = get_object_or_404(Post, id=pk)
    total_likes = stuff.total_likes()
    total_saves = stuff.total_saves()
    total_comments = stuff.comments.all().filter(reply=None).order_by('-id')
    total_comments2 = stuff.comments.all().order_by('-id')
    context = {}
    if request.method == "POST":
        comment_qs = None
        comment_form = CommentForm(request.POST or None)
        if comment_form.is_valid():
            form = request.POST.get('body')
            reply_id = request.POST.get('comment_id')
            if reply_id:
                comment_qs = Comment.objects.get(id=reply_id)
            comment = Comment.objects.create(name=request.user,post=stuff,body=form, reply=comment_qs)
            comment.save()
            if reply_id:
                notify = Notification(post=stuff, sender=request.user, user=stuff.author, text_preview=form, notification_type=4)
                notify.save()
            else:
                notify = Notification(post=stuff, sender=request.user, user=stuff.author, text_preview=form, notification_type=3)
                notify.save()
            total_comments = stuff.comments.all().filter(reply=None).order_by('-id')
            total_comments2 = stuff.comments.all().order_by('-id')
    else:
        comment_form = CommentForm()

    tcl={}
    for cmt in total_comments2:
        total_clikes = cmt.total_clikes()
        cliked = False
        if cmt.likes.filter(id=request.user.id).exists():
            cliked = True
        tcl[cmt.id] = cliked
    context["clikes"]=tcl

    liked = False
    if stuff.likes.filter(id=request.user.id).exists():
        liked = True
    context["total_likes"]=total_likes
    context["liked"]=liked

    saved = False
    if stuff.saves.filter(id=request.user.id).exists():
        saved = True
    context["total_saves"]=total_saves
    context["saved"]=saved
    context['comment_form'] = comment_form
    context['post']=stuff
    context['comments']=total_comments

    if is_ajax(request=request):
        html = render_to_string('blog/comments.html',context, request=request)
        return JsonResponse({'form':html})

    return render(request, 'blog/post_detail.html', context)

""" Crear post """
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields =['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


""" Actualizar post """
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields =['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

""" Borrar post """
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

""" Página de información """
def about(request):
    return render(request, 'blog/about.html', {'title':'About'})


""" Buscar por título/usuario """
def search(request):
    query = request.GET['query']
    if len(query) >= 150 or len(query) < 1:
        allposts = Post.objects.none()
    elif len(query.strip()) == 0:
        allposts = Post.objects.none()
    else:
        allpostsTitle = Post.objects.filter(title__icontains=query)
        allpostsAuthor = Post.objects.filter(author__username = query)
        allposts = allpostsAuthor.union(allpostsTitle)
    params = {'allposts': allposts}
    return render(request, 'blog/search_results.html', params)


""" Posts favoritos """
@login_required
def AllLikeView(request):
    user = request.user
    liked_posts = user.blogpost.all()
    return render(request, 'blog/liked_posts.html', {'liked_posts':liked_posts})


""" Posts guardados """
@login_required
def AllSaveView(request):
    user = request.user
    saved_posts = user.blogsave.all()
    return render(request, 'blog/saved_posts.html', {'saved_posts':saved_posts})