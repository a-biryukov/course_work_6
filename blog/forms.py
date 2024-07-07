from django import forms

from blog.models import Blog
from mailings.forms import StyleFormMixin


class BlogForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = Blog
        exclude = ("views_count", "slug", "author", "is_published",)


class BlogModeratorForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = Blog
        exclude = ("views_count", "slug", "author", "author",)
