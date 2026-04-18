from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.utils import timezone

from artists.models import Artist
from blog.models import Post
from gallery.models import Artwork, Category

from .utils_assets import save_uploaded_image


class StaffAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update(
            {"class": "login-field", "autocomplete": "username", "placeholder": "Username"}
        )
        self.fields["password"].widget.attrs.update(
            {
                "class": "login-field",
                "autocomplete": "current-password",
                "placeholder": "Password",
            }
        )


_dash = {"class": "dash-input"}
_dash_ta = {"class": "dash-input dash-input--textarea"}


class ArtistForm(forms.ModelForm):
    class Meta:
        model = Artist
        fields = ("name",)
        widgets = {"name": forms.TextInput(attrs=_dash)}


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ("name",)
        widgets = {"name": forms.TextInput(attrs=_dash)}


class DashboardPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("title", "content", "artist", "post_date")
        widgets = {
            "title": forms.TextInput(attrs=_dash),
            "content": forms.Textarea(attrs={**_dash_ta, "rows": 6}),
            "artist": forms.Select(attrs=_dash),
            "post_date": forms.DateTimeInput(
                attrs={**_dash, "type": "datetime-local"},
                format="%Y-%m-%dT%H:%M",
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["post_date"].input_formats = (
            "%Y-%m-%dT%H:%M",
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%d %H:%M:%S%z",
        )
        if self.instance.pk:
            dt = timezone.localtime(self.instance.post_date)
            self.initial.setdefault("post_date", dt.strftime("%Y-%m-%dT%H:%M"))
        else:
            now = timezone.localtime(timezone.now())
            self.initial.setdefault("post_date", now.strftime("%Y-%m-%dT%H:%M"))


class DashboardArtworkForm(forms.ModelForm):
    image_file = forms.FileField(
        required=False,
        validators=[
            FileExtensionValidator(
                allowed_extensions=["jpg", "jpeg", "png", "webp", "gif"]
            )
        ],
        help_text="Images are stored in the assets folder with a unique name.",
    )

    class Meta:
        model = Artwork
        fields = ("title", "description", "category", "artist")
        widgets = {
            "title": forms.TextInput(attrs=_dash),
            "description": forms.Textarea(attrs={**_dash_ta, "rows": 4}),
            "category": forms.Select(attrs=_dash),
            "artist": forms.Select(attrs=_dash),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields["image_file"].help_text = (
                "Optional — upload a new file to replace "
                f"“{self.instance.image_path}”."
            )

    def clean(self):
        cleaned = super().clean()
        if not self.instance.pk and not cleaned.get("image_file"):
            raise ValidationError(
                {"image_file": "Please upload an image for a new artwork."}
            )
        return cleaned

    def save(self, commit=True):
        obj = super().save(commit=False)
        f = self.cleaned_data.get("image_file")
        if f:
            obj.image_path = save_uploaded_image(f)
        if commit:
            obj.save()
        return obj
