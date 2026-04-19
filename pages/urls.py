from django.urls import path
from django.views.generic import TemplateView

from . import views

app_name = "pages"

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("gallery/", views.gallery_page, name="gallery"),
    # More specific path first (before `inspiration/`).
    path(
        "inspiration/post/<int:pk>/",
        views.inspiration_post,
        name="inspiration_post",
    ),
    path("inspiration/", views.inspiration, name="inspiration"),
    path(
        "pages/",
        TemplateView.as_view(template_name="pages/gallery/art_gallery.html"),
        name="legacy_showcase",
    ),
    path(
        "pages/fabiola-morcillo/",
        TemplateView.as_view(template_name="pages/gallery/fabiola_morcillo.html"),
        name="fabiola",
    ),
    path(
        "pages/valentin-pavageau/",
        TemplateView.as_view(template_name="pages/gallery/valentin_pavageau.html"),
        name="valentin",
    ),
    path(
        "pages/butcher-billy/",
        TemplateView.as_view(template_name="pages/gallery/butcher_billy.html"),
        name="butcher_billy",
    ),
    path(
        "pages/david-sosella/",
        TemplateView.as_view(template_name="pages/gallery/david_sosella.html"),
        name="david",
    ),
    path(
        "pages/kyle-lambert/",
        TemplateView.as_view(template_name="pages/gallery/kyle_lambert.html"),
        name="kyle",
    ),
]
