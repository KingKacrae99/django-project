
from django.urls import path
from . import views


urlpatterns = [
    path('', views.homepage, name= 'home'),
    path('notification', views.notifications_view, name='notification'),
    path('Article/read_notifications/<int:notification_id>', views.mark_as_read_notification, name='read'),
    path('notification/mark_all_read/', views.mark_all_as_read, name='all_read'),
    path('login/', views.loginpage, name = 'Login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerpage, name = 'Register'),

    path('dashboard/',views.dashboard, name= 'dashboard'),
    path('user/', views.profilepage, name = 'user'),
    path('profile/<int:pk>', views.View_Profile, name ='view_profile'),
    path('gallery/',views.UserGallery, name='gallery'),

    # Settings View
    path('settings/', views.profile_settings, name= 'settings'),
    path('settings/privacy/<int:pk>', views.PrivacySettings, name='privacy'),
    path('settings/change_password', views.ChangePassword, name = 'change_password'),
    path('setting/notification', views.notify_settings, name='notify_settings'),
    path('settings/post', views.post_settings, name='post_setting'),
    path('settings/activate&deactivate', views.activation_settings, name='activate_setting'),
    
    # POST-VIEW
    path('post/', views.PostPage, name = "post"),
    path('Article/<slug:slug>', views.singlepost, name ="article"),
    path('create_post/', views.CreatePost, name = "postform"),
    path('update_post/<str:pk>', views.UpdatePost, name = "updatepost"),
    path('delete_post/<str:pk>', views.DeletePost, name='delete_post'),

    #Liked view
    path('like_post/<int:pk>', views.LikePost, name="like_post"),

    #Comment View
    path('Article/<int:pk>/create_comments', views.CreatComment, name='create_comment'),
    path('Article/<int:pk>/update_comments', views.UpdateComment, name='update_comment'),
    path('publish_post/<slug:slug>/', views.PublishedStatus, name='publish_post'),
    path('delete_comment/<int:pk>', views.DeleteComment, name='delete_comment'),
    path('Sports/',views.sportpage, name='sport'),
    path('News/',views.Newspage, name='news'),
    path('business/',views.Businesspage, name='business'),
    path('Education/',views.Educationpage, name='education'),
    path('Science/',views.Sciencepage, name='science'),
    path('Technology/',views.Techpage, name='tech'),
    path('SoftwareDev/',views.Programmeringpage, name='programming'),
    path('Health/',views.Healthpage, name='health'),
    path('Entertainment/',views.Entpage, name='ent'),
]
