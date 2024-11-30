from django.urls import include, path
from django.views.generic.base import RedirectView
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("groups", RedirectView.as_view(pattern_name="index"), name="groups_redirect"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register_view, name="register"),
    path("create-group", views.create_group, name="create_group"),
    path("groups/<str:group_id>", views.group, name="group"),
    path("groups/<str:group_id>/<str:section>", views.group, name="group_section"),
    path("__reload__", include("django_browser_reload.urls")),
]
