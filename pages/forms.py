from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.utils import timezone

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


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ("name",)
        widgets = {"name": forms.TextInput(attrs=_dash)}


class DashboardPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("title", "content")
        widgets = {
            "title": forms.TextInput(attrs=_dash),
            "content": forms.Textarea(attrs={**_dash_ta, "rows": 6}),
        }

    def save(self, commit=True):
        obj = super().save(commit=False)
        if not obj.pk:
            obj.post_date = timezone.now()
        if commit:
            obj.save()
        return obj


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
        fields = ("title", "description", "category")
        widgets = {
            "title": forms.TextInput(attrs=_dash),
            "description": forms.Textarea(attrs={**_dash_ta, "rows": 4}),
            "category": forms.Select(attrs=_dash),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["image_file"].widget = forms.FileInput(
            attrs={
                "class": "dash-file-input",
                "accept": ".jpg,.jpeg,.png,.webp,.gif,image/jpeg,image/png,image/webp,image/gif",
            }
        )
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
