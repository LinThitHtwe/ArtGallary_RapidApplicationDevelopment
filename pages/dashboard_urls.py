from django.urls import path

from . import dashboard_views

app_name = "dashboard"

urlpatterns = [
    path("login/", dashboard_views.StaffLoginView.as_view(), name="login"),
    path("logout/", dashboard_views.StaffLogoutView.as_view(), name="logout"),
    path("", dashboard_views.dashboard_home, name="home"),
    path("categories/", dashboard_views.category_list, name="category_list"),
    path(
        "categories/<int:pk>/edit/",
        dashboard_views.category_edit,
        name="category_edit",
    ),
    path(
        "categories/<int:pk>/delete/",
        dashboard_views.category_delete,
        name="category_delete",
    ),
    path("posts/", dashboard_views.post_list, name="post_list"),
    path("posts/new/", dashboard_views.post_create, name="post_create"),
    path("posts/<int:pk>/edit/", dashboard_views.post_edit, name="post_edit"),
    path("posts/<int:pk>/delete/", dashboard_views.post_delete, name="post_delete"),
    path("artworks/", dashboard_views.artwork_list, name="artwork_list"),
    path("artworks/new/", dashboard_views.artwork_create, name="artwork_create"),
    path("artworks/<int:pk>/edit/", dashboard_views.artwork_edit, name="artwork_edit"),
    path(
        "artworks/<int:pk>/delete/",
        dashboard_views.artwork_delete,
        name="artwork_delete",
    ),
]
