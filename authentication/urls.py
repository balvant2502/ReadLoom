from django.urls import path

from . import views


urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("register/", views.register_view, name="register"),
    path("logout/", views.logout_view, name='logout'),
    path("user_dashboard/", views.user_dashboard_view, name='dashboard'),
    path("author_dashboard/", views.author_dashboard_view, name='author_dashboard'),
    path("admin_dashboard/", views.admin_dashboard_view, name='admin_dashboard'),
    path("profile_update/", views.profile_update_view, name='profile_update'),
    
]