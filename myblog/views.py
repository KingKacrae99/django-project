from django.db.models import Count,Q
from django.db.models.functions import ExtractMonth
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .form import SignUpForm, LoginForm, PostForm, PrivacySettingForm
from django.contrib.auth import authenticate, login, logout
from .models import *
from django.utils import timezone
from django.urls import reverse
from django.http import HttpResponseRedirect, Http404
from .permission import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
import json, random
# Create your views here.

def homepage(request):
    published_post= Post.objects.filter(status='published').order_by('-dop')[:50]
    now = timezone.now()

    one_hour = now - timezone.timedelta(hours=1)
    breaking_news = Post.objects.filter(status='published', dop__gte=one_hour )
    context = {
        'published_post': published_post,
        'breaking_news': breaking_news
    }
    return render(request, 'blog/main.html', context)

def sportpage(request):
    published_post= Post.objects.filter(category__name='Sports').order_by('-dop')
    context = {
        'published_post': published_post
    }
    return render(request,'blog/main.html', context)

def Newspage(request):
    published_post= Post.objects.filter(category__name='News').order_by('-dop')
    context = {
        'published_post': published_post
    }
    return render(request,'blog/main.html', context)


def Businesspage(request):
    published_post= Post.objects.filter(category__name='Business').order_by('-dop')
    context = {
        'published_post': published_post
    }
    return render(request,'blog/main.html', context)

def Educationpage(request):
    published_post= Post.objects.filter(category__name='Education').order_by('-dop')
    context = {
        'published_post': published_post
    }
    return render(request,'blog/main.html', context)

def Sciencepage(request):
    published_post= Post.objects.filter(category__name='Science').order_by('-dop')
    context = {
        'published_post': published_post
    }
    return render(request,'blog/main.html', context)

def Techpage(request):
    published_post= Post.objects.filter(category__name='Technology').order_by('-dop')
    context = {
        'published_post': published_post
    }
    return render(request,'blog/main.html', context)

def Programmeringpage(request):
    published_post= Post.objects.filter(category__name='programming').order_by('-dop')
    context = {
        'published_post': published_post
    }
    return render(request,'blog/main.html', context)

def Healthpage(request):
    published_post= Post.objects.filter(category__name='Health').order_by('-dop')
    context = {
        'published_post': published_post
    }
    return render(request,'blog/main.html', context)

def Entpage(request):
    published_post= Post.objects.filter(category__name='Entertainment').order_by('-dop')
    context = {
        'published_post': published_post
    }
    return render(request,'blog/main.html', context)

def notifications_view(request):
    if request.user.is_authenticated:
        unread_nofitications = request.user.notifications.filter(is_read=False)
        notifications = request.user.notifications.all().order_by('-timestamp')[:10]
        total_unread = unread_nofitications.count()

    else:
        notifications = []
        total_unread = 0

    context={
        'total_unread': total_unread,
        'notifications': notifications,
    }
    return context

def mark_all_as_read(request):
    unread_nofitications = request.user.notifications.filter(is_read=False)
    if request.user.is_authenticated:
            unread_nofitications.update(is_read = True)
    return redirect('user')

def mark_as_read_notification(request, notification_id):
    read_notification = get_object_or_404(Notification, id=notification_id)
    if read_notification.recipient == request.user:
        read_notification.is_read = True
        read_notification.save()
    return redirect('article', slug=read_notification.post.slug )



@unauthenticated
def loginpage(request):
    latest_post = Post.objects.filter(status='published').order_by('-dop')[:10]

    if latest_post.exists():
        random_post = random.sample(list(latest_post), min(len(latest_post), 3))

    form = LoginForm(request.POST)
    msg ="Welcome!"
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                msg= 'successful'
                login(request, user)
                return redirect('user')
            else:
                msg = 'account doe not exist'
        else:
           msg= 'error validating forms'

    context = {
        'form': form,
        'msg':msg,
        'random_post': random_post,
    }
    return render(request, 'blog/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('Login')

@unauthenticated
def registerpage(request):
    msg = None
    if request.method == 'POST':
        role = User.objects.filter(role='user')
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            msg = 'User created successfully.'
            return redirect('Login')
        else:
            msg = 'Form is not valid. Please check the errors.'
    else:
        form = SignUpForm()

    context = {
        'form': form,
        'msg': msg  # Pass the message to the template
    }
    return render(request, 'blog/register.html', context)

@login_required(login_url='Login')
@only_admin
def dashboard(request):
    all_user = User.objects.all()
    posts = Post.objects.all()
    user = User.objects.filter(role='author')
    post = Post.objects.filter(status='published')
    draft_post = Post.objects.filter(status='draft')

    #Group Users by the month they registered
    monthly_data = User.objects.annotate(month=ExtractMonth('date_joined')).values('month').annotate(
        registered=Count('id'),
        active=Count('id', filter=Q(is_active=True)),
        inactive=Count('id',filter=Q(is_active=False))
    )
    chart_data = {month:{'registered':0,'active':0,'inactive':0 } for month in range(1,13)}
    for data in monthly_data:
        chart_data[data['month']] = {
            'registered':data['registered'],
            'active':data['active'],
            'inactive':data['inactive'],
        }

    #filter active and inactive users
    active_user = User.objects.filter(is_active=True).count()
    inactive_user = User.objects.filter(is_active=False).count()
    total_user =all_user.count()

    total_post = posts.count()
    total_author = user.count()
    published = post.count()
    unpublished = draft_post.count()

    context = {
        'author': total_author,
        'published': published,
        'unpublished': unpublished,
        'total_post':total_post,
        'not_post': draft_post,
        'news': post,
        'total_user': total_user,
        'active': active_user,
        'inactive': inactive_user,
        'months': list(chart_data.keys()),
        'registrations': [chart_data[month]['registered'] for month in chart_data],
        'active_users': [chart_data[month]['active'] for month in chart_data],
        'inactive_users': [chart_data[month]['inactive'] for month in chart_data],
    }

    return render(request, 'blog/dashboard.html', context)


@login_required(login_url='Login')
@allow_users(roles=[ 'author', 'user'])
def profilepage(request):
    mypost = Post.objects.filter(author=request.user)
    posts= Post.objects.filter(status='published').order_by('-dop')

    context = {
        'mypost': mypost,
        'posts': posts,
    }
    return render(request, 'blog/user.html', context)

def View_Profile(request, pk):
    target_user = get_object_or_404(User, pk=pk)
    allow_view = target_user.settings.allow_view
    posts = Post.objects.filter(author=target_user, status='published')


    if allow_view:
        user_can_view = (
            request.user.is_authenticated and (request.user== target_user or request.user.is_authenticated)
        )
    else:
        user_can_view = True

    if request.method == 'POST':
        target_user.is_active = not target_user.is_active
        target_user.save()
        return redirect('view_profile', pk=pk)


    context = {
        'target_user': target_user,
        'user_can_view': user_can_view,
        'posts': posts if user_can_view else None,
        'email': target_user.email if target_user.settings.show_email else None,
    }

    return render(request, 'blog/view_profile.html', context)

def UserGallery(request):
    if request.user.is_authenticated:
        mypost = Post.objects.filter(author=request.user,status='published')
        draft= Post.objects.filter(author=request.user, status='draft')
        sum_post= Post.objects.filter(author=request.user)

        filtered=  mypost.count()
        total_draft = draft.count()
        total_post = sum_post.count()
    else:
        return redirect('Login')
    context = {
        'mypost': mypost,
        'filtered': filtered,
        'total_draft': total_draft,
        'total_post': total_post
    }
    return render(request, 'blog/gallery.html', context)

def profile_settings(request):
    role_choices = User._meta.get_field('role').choices
    user = User.objects.get(id=request.user.id)

    if request.method == 'POST':
        username = request.POST.get("username", user.username)
        first_name = request.POST.get("first_name", user.first_name)
        last_name = request.POST.get("last_name", user.last_name)
        email = request.POST.get("email", user.email)
        location = request.POST.get("location", user.location)
        bio = request.POST.get("bio", user.bio)
        job = request.POST.get("job", user.job)
        profile_picture = request.FILES.get("profile_picture", user.profile_picture)
        password = request.POST.get("password")
        role = request.POST.get("role", user.role)

        valid_role = dict(user._meta.get_field('role').choices).keys()

        if not username or not email:
            messages.error(request, "username and email are required.")
            return redirect('profile_setting')
        elif not password:
            messages.error(request, "Password is required to confirm your profile Update.")

        # updated Profile
        user.username= username
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.location = location
        user.bio = bio
        user.job = job

        if role not in valid_role:
            messages.error(request, "Invalid role selected.")
        else:
            user.role = role
        
        if profile_picture:
            user.profile_picture = profile_picture

        user.save()
        messages.success(request, "Updated Profile Successfully.")
        return redirect('user')


    context = {
        'choices': role_choices,
        'user': user

    }
    return render(request, 'blog/settings.html', context)

@login_required
def PrivacySettings(request, pk):
    if request.user.is_authenticated:
        target_user = get_object_or_404(User, id=pk)
        if request.user != target_user:
            return HttpResponseForbidden('Not Authorized')
            
        user_settings, created = UserSettings.objects.get_or_create(user=target_user)

        if request.method == 'POST':
            show_email = request.POST.get('show_emails') == 'on'
            allow_views = request.POST.get('allow_views') == 'on'
           
            # Update only if there is a change
            if user_settings.show_email != show_email:
                user_settings.show_email = show_email
            if user_settings.allow_view != allow_views:
                user_settings.allow_view = allow_views

            user_settings.save()
            print(f"POST data: {request.POST}")
            print(f"show_email before save: {request.POST.get('show_emails')}")
            print(f"allow_view before save: {request.POST.get('allow_views')}")
            print(user_settings.show_email)
            print(user_settings.allow_view)
            return redirect('settings')
        else:
            intial_data = {
                'show_email': user_settings.show_email,
                'allow_view': user_settings.allow_view,
            }
            form = PrivacySettingForm(initial=intial_data)
            print("action took place here")

    print(user_settings.show_email)
    context = {
        'user': target_user,
        'setting': user_settings
    }
    return render(request, 'blog/settings.html', context)

@login_required
def notify_settings(request):
    if request.method == 'POST':
        notify_email = request.POST.get("email_notifications")=="on"

        user_setings = request.user.settings
        user_setings.email_notification = notify_email

        user_setings.save()

        messages.success(request,"Notifications settings updated successfully")
        return redirect('notify_settings')
    
    return render(request, 'blog/settings.html')

def post_settings(request):
    user = request.user
    my_posts = Post.objects.filter(author=user)

    if request.method == 'POST':
        post_id = request.POST.get("user_post")
        take_down = request.POST.get("unpublished")

        if post_id:
            try:
                post = Post.objects.get(id=post_id, author=user)

                if take_down:
                    post.status ='draft'
                    post.save()
                    return messages.success(request, f"The post '{post.title}' has been taken down")
                else:
                    return messages.info(request, f"No action taken for the post '{post.title}'.")
            except Post.DoesNotExist:
                return messages.error(request, "Post not found or you do not have permission to modify it")
        else:
            return messages.error(request, "Please select a valid post")
    print(my_posts)
    context = {
        'my_posts': my_posts
        }
    return render(request, 'blog/settings.html', context)

def activation_settings(request):
    try:
        user = User.objects.get(id=request.user.id)
        if  request.method == 'POST':
            acct_mode = request.POST.get("mode")=='on'
            password = request.POST.get("password")
            print(request.POST)

            if user.check_password(password):
                user.is_active = acct_mode
                user.save()
                messages.success(request, f"Settings successfully Updated!!")
            else:
                messages.error(request, "Incorrect password. Please try again.")
            
            return redirect('home')
    except User.DoesNotExist:
         messages.error(request, f"The account with not found. Pls contact the adminstrator.")
    return render(request, 'blog/settings.html')

def PostPage(request):
    posts = Post.objects.filter(status='published')
    recent_post = Post.objects.filter(status='published').order_by('-dop')[:5]
    trending= []

    for post in posts:
        if post.likes.count() >= 3:
            post.is_trending=True
            post.save()
            trending.append(post)
        else:
            post.is_trending =False
            post.save()

    context={
        'trends':trending,
        'recent_post': recent_post,
      }
    return render(request, 'blog/post.html', context)

def singlepost(request, slug):
    mypost = Post.objects.get(slug=slug)
    total_likes = mypost.likes.count()
    comments = Comment
    liked= False
    if mypost.likes.filter(id=request.user.id).exists():
        liked = True

    context={
        'mypost': mypost,
        'comments':comments,
        'total_likes': total_likes,
        'liked': liked

    }
    return render(request, 'blog/single_post.html', context)

@login_required(login_url='Login')
def LikePost(request,pk):
    mypost = get_object_or_404(Post, id=pk)
    liked = False
    if mypost.likes.filter(id=request.user.id).exists():
        mypost.likes.remove(request.user)
        liked = False
    else:
        mypost.likes.add(request.user)

        if mypost.author != request.user:
            Notification.objects.create(
                recipient = mypost.author,
                sender= request.user,
                notification_type = 'like',
                post= mypost,
                message = f"{request.user.username} liked your post '{mypost.title}'."
            )
    return HttpResponseRedirect(reverse('article', args=[mypost.slug]))

@login_required(login_url='Login')
@allow_users(roles=['author'])
def CreatePost(request):
    form =PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid:
            form.save()
            return redirect('post')
        else:
            msg= 'Pls fill up the form'
    else:
       form = PostForm()

    context ={
        'form': form
    }
    return render(request, 'blog/postform.html', context)

@login_required(login_url='Login')
@allow_users(roles=['author'])
def UpdatePost(request, pk):
    mypost = Post.objects.get(id=pk)
    form =PostForm(instance=mypost)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=mypost)
        if form.is_valid:
            form.save()
            return redirect('post')

    context= {'form':form}
    return render(request, 'blog/postform.html', context)

@login_required(login_url='Login')
@only_admin
def PublishedStatus(request, slug):
    if not slug:
        return JsonResponse({'status': 'error', 'message': 'Invalid slug'}, status=400)
    
    if request.method =='POST':
        post = get_object_or_404(Post, slug=slug)
        post.status = 'published'
        post.save()
        return redirect('publish_post', slug=post.slug)
    return redirect('dashboard')

@login_required(login_url='Login')
@allow_users(roles=['author'])
def DeletePost(request,pk):
    mypost = Post.objects.get(id=pk)
    if request.method == 'POST':
        mypost.delete()
        return redirect('profile')

    context = {
        'mypost': mypost
        }
    return render(request, 'blog/deletepost.html', context)

@login_required(login_url='Login')
def CreatComment(request,pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        user = request.user
        comment_body = request.POST.get('comment')


        Comment.objects.create(
            post = post,
            user =user,
            comment_body = comment_body,
            date=timezone.now()
        )
        return redirect('article',slug=post.slug)
    
    context= {
        'post':post,
        'comment':None
    }
    
    return render(request, 'blog/commentform.html', context)

@login_required(login_url='Login')
def UpdateComment(request,pk):
    comment = Comment.objects.get(id=pk)
    post = comment.post
    if request.method == 'POST':
        comment_body = request.POST.get('comment')
        comment.comment_body = comment_body
        comment.date= timezone.now()
        if comment is not None:
            comment.save()
            return redirect('article', slug=comment.post.slug)
    
    context ={
        'comment': comment,
        'post': post
    }
    return render(request, 'blog/Update_comment.html', context)

@login_required(login_url='Login')
def DeleteComment(request,pk):
    comment= Comment.objects.get(id=pk)
    article_slug = comment.post.slug
    if request.method == "POST":
        post_slug= comment.post.slug
        comment.delete()
        return redirect('article', slug=post_slug)
    
    context ={
        'comment':comment,
        'slug': article_slug
    }
    return render(request, 'blog/delete_comment.html', context)

@login_required
def ChangePassword(request):
    user = request.user
    msg = None

    if request.method == 'POST':
        current_password = request.POST.get("old_password")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("new_password2")

        if not check_password(current_password, user.password):
            msg = "old password is incorrect!"
        elif current_password == new_password:
            msg = "The new password cannot be the same as the current password."
        elif new_password != confirm_password:
             msg = "The new password and confirm password do not match."
        else:
            user.set_password(new_password)
            update_session_auth_hash(request, user)  # Keeps the user logged in after password change
            user.save()
            msg = "Password successfully changed!"
            return redirect('settings')
        
        context = {
            'msg': msg
        }
    
    return render(request, 'blog/settings.html', context)

