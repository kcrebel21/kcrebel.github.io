from django.urls import path
from . import views
from .views import UserProfileViewSet
from rest_framework.routers import DefaultRouter
from django.conf.urls.static import static
from .views import user_logout
from .views import delete_thread

from django.contrib.auth import views as auth_views

router = DefaultRouter()
router.register(r'userprofiles', UserProfileViewSet)

urlpatterns = [
    path('', views.thread_list, name='thread_list'),
    path('<int:thread_id>/', views.thread_detail, name='thread_detail'),
    path('new/', views.new_thread, name='new_thread'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup, name='signup'),
    path('profile/', views.user_profile, name='user_profile'),
    path('logout/', user_logout, name='logout'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('comment/<int:comment_id>/edit/', views.edit_comment, name='edit_comment'),
    path('comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
    path('thread/<int:thread_id>/delete/', delete_thread, name='delete_thread'),
    
]


