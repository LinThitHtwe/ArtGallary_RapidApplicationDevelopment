from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.views import LoginView, LogoutView
from django.db.models import Count
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render

from artists.models import Artist
from blog.models import Post
from gallery.models import Artwork, Category

from .forms import (
    ArtistForm,
    CategoryForm,
    DashboardArtworkForm,
    DashboardPostForm,
    StaffAuthenticationForm,
)


def staff_required(view_func):
    checker = user_passes_test(lambda u: u.is_authenticated and u.is_staff)
    return login_required(checker(view_func))


class StaffLoginView(LoginView):
    template_name = "pages/dashboard/login.html"
    authentication_form = StaffAuthenticationForm
    redirect_authenticated_user = False

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_staff:
                return redirect("dashboard:home")
            messages.error(
                request,
                "Staff access only. This account cannot open the dashboard.",
            )
            return redirect("pages:home")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.get_user()
        if not user.is_staff:
            messages.error(
                self.request,
                "Staff access only. Sign in with a staff account (is_staff=True).",
            )
            return redirect("dashboard:login")
        login(self.request, user)
        return HttpResponseRedirect(self.get_success_url())


class StaffLogoutView(LogoutView):
    next_page = "/"


@staff_required
def dashboard_home(request):
    counts = {
        "artists": Artist.objects.count(),
        "posts": Post.objects.count(),
        "artworks": Artwork.objects.count(),
        "categories": Category.objects.count(),
    }
    recent_art = Artwork.objects.select_related("category").order_by("-id")[:6]
    recent_posts = Post.objects.select_related("artist").order_by("-post_date")[:6]
    return render(
        request,
        "pages/dashboard/home.html",
        {
            "counts": counts,
            "recent_art": recent_art,
            "recent_posts": recent_posts,
            "dash_section": "overview",
        },
    )


# ——— Artists ———


@staff_required
def artist_list(request):
    artists = Artist.objects.annotate(
        _works=Count("artworks"), _posts=Count("posts")
    ).order_by("name")
    return render(
        request,
        "pages/dashboard/artist_list.html",
        {"artists": artists, "dash_section": "artists"},
    )


@staff_required
def artist_create(request):
    form = ArtistForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Artist created.")
        return redirect("dashboard:artist_list")
    return render(
        request,
        "pages/dashboard/artist_form.html",
        {"form": form, "dash_section": "artists", "editing": False},
    )


@staff_required
def artist_edit(request, pk):
    artist = get_object_or_404(Artist, pk=pk)
    form = ArtistForm(request.POST or None, instance=artist)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Artist updated.")
        return redirect("dashboard:artist_list")
    return render(
        request,
        "pages/dashboard/artist_form.html",
        {"form": form, "artist": artist, "dash_section": "artists", "editing": True},
    )


@staff_required
def artist_delete(request, pk):
    artist = get_object_or_404(Artist, pk=pk)
    if request.method == "POST":
        name = artist.name
        artist.delete()
        messages.success(request, f"Deleted artist “{name}”.")
        return redirect("dashboard:artist_list")
    return render(
        request,
        "pages/dashboard/artist_confirm_delete.html",
        {"artist": artist, "dash_section": "artists"},
    )


# ——— Categories ———


@staff_required
def category_list(request):
    categories = Category.objects.annotate(_n=Count("artworks")).order_by("name")
    form = CategoryForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Category added.")
        return redirect("dashboard:category_list")
    return render(
        request,
        "pages/dashboard/category_list.html",
        {
            "categories": categories,
            "form": form,
            "dash_section": "categories",
        },
    )


@staff_required
def category_delete(request, pk):
    cat = get_object_or_404(Category, pk=pk)
    if request.method == "POST":
        name = cat.name
        cat.delete()
        messages.success(request, f"Deleted category “{name}”.")
        return redirect("dashboard:category_list")
    return render(
        request,
        "pages/dashboard/category_confirm_delete.html",
        {"category": cat, "dash_section": "categories"},
    )


# ——— Posts ———


@staff_required
def post_list(request):
    posts = Post.objects.select_related("artist").order_by("-post_date", "-id")
    return render(
        request,
        "pages/dashboard/post_list.html",
        {"posts": posts, "dash_section": "posts"},
    )


@staff_required
def post_create(request):
    form = DashboardPostForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Post published.")
        return redirect("dashboard:post_list")
    return render(
        request,
        "pages/dashboard/post_form.html",
        {"form": form, "dash_section": "posts", "editing": False},
    )


@staff_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    form = DashboardPostForm(request.POST or None, instance=post)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Post updated.")
        return redirect("dashboard:post_list")
    return render(
        request,
        "pages/dashboard/post_form.html",
        {"form": form, "post": post, "dash_section": "posts", "editing": True},
    )


@staff_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        title = post.title
        post.delete()
        messages.success(request, f"Deleted post “{title}”.")
        return redirect("dashboard:post_list")
    return render(
        request,
        "pages/dashboard/post_confirm_delete.html",
        {"post": post, "dash_section": "posts"},
    )


# ——— Artworks ———


@staff_required
def artwork_list(request):
    works = Artwork.objects.select_related("category", "artist").order_by(
        "-id",
    )
    return render(
        request,
        "pages/dashboard/artwork_list.html",
        {"artworks": works, "dash_section": "artworks"},
    )


@staff_required
def artwork_create(request):
    form = DashboardArtworkForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Artwork added — image saved under assets/.")
        return redirect("dashboard:artwork_list")
    return render(
        request,
        "pages/dashboard/artwork_form.html",
        {"form": form, "dash_section": "artworks", "editing": False},
    )


@staff_required
def artwork_edit(request, pk):
    artwork = get_object_or_404(Artwork, pk=pk)
    form = DashboardArtworkForm(
        request.POST or None, request.FILES or None, instance=artwork
    )
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Artwork updated.")
        return redirect("dashboard:artwork_list")
    return render(
        request,
        "pages/dashboard/artwork_form.html",
        {
            "form": form,
            "artwork": artwork,
            "dash_section": "artworks",
            "editing": True,
        },
    )


@staff_required
def artwork_delete(request, pk):
    artwork = get_object_or_404(Artwork, pk=pk)
    if request.method == "POST":
        title = artwork.title
        artwork.delete()
        messages.success(request, f"Deleted artwork “{title}”.")
        return redirect("dashboard:artwork_list")
    return render(
        request,
        "pages/dashboard/artwork_confirm_delete.html",
        {"artwork": artwork, "dash_section": "artworks"},
    )
