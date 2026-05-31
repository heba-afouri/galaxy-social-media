from django import forms

from posts.models import Post
from groups.models import Group


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("message", "group")

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        self.fields["group"].required = False
        self.fields["group"].empty_label = "— No galaxy (public post) —"
        if user is not None:
            # Only offer galaxies the user belongs to.
            self.fields["group"].queryset = Group.objects.filter(
                pk__in=user.user_groups.values_list("group__pk", flat=True)
            )
