from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.views import LoginView, LogoutView
from django.db.models import Count
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render

from blog.models import Post
from gallery.models import Artwork, Category

from .forms import (
    CategoryForm,
    DashboardArtworkForm,
    DashboardPostForm,
    StaffAuthenticationForm,
    get_site_artist,
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
                "This account cannot open the private studio area.",
            )
            return redirect("pages:home")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.get_user()
        if not user.is_staff:
            messages.error(
                self.request,
                "That sign-in does not have access to the studio tools.",
            )
            return redirect("dashboard:login")
        login(self.request, user)
        return HttpResponseRedirect(self.get_success_url())


class StaffLogoutView(LogoutView):
    next_page = "/"


@staff_required
def dashboard_home(request):
    counts = {
        "posts": Post.objects.count(),
        "artworks": Artwork.objects.count(),
        "categories": Category.objects.count(),
    }
    recent_art = Artwork.objects.select_related("category").order_by("-id")[:8]
    recent_posts = Post.objects.order_by("-post_date")[:6]
    site_artist = get_site_artist()
    return render(
        request,
        "pages/dashboard/home.html",
        {
            "counts": counts,
            "recent_art": recent_art,
            "recent_posts": recent_posts,
            "site_artist_name": site_artist.name,
            "dash_section": "overview",
        },
    )


# ——— Categories ———


@staff_required
def category_list(request):
    categories = Category.objects.annotate(artwork_count=Count("artworks")).order_by(
        "name"
    )
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
    if request.method != "POST":
        return redirect("dashboard:category_list")
    name = cat.name
    cat.delete()
    messages.success(request, f"Deleted category “{name}”.")
    return redirect("dashboard:category_list")


# ——— Posts ———


@staff_required
def post_list(request):
    posts = Post.objects.order_by("-post_date", "-id")
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
        messages.success(request, "Journal entry published.")
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
        messages.success(request, "Journal entry updated.")
        return redirect("dashboard:post_list")
    return render(
        request,
        "pages/dashboard/post_form.html",
        {"form": form, "post": post, "dash_section": "posts", "editing": True},
    )


@staff_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method != "POST":
        return redirect("dashboard:post_list")
    title = post.title
    post.delete()
    messages.success(request, f"Removed journal entry “{title}”.")
    return redirect("dashboard:post_list")


# ——— Artworks ———


@staff_required
def artwork_list(request):
    works = Artwork.objects.select_related("category").order_by("-id")
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
        messages.success(request, "Artwork added to the gallery.")
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
    if request.method != "POST":
        return redirect("dashboard:artwork_list")
    title = artwork.title
    artwork.delete()
    messages.success(request, f"Deleted artwork “{title}”.")
    return redirect("dashboard:artwork_list")
