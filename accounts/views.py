from django.contrib import messages
from django.contrib.auth import login, logout, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views import generic

from . import forms

AUTH_BACKEND = "django.contrib.auth.backends.ModelBackend"


class SignUp(generic.CreateView):
    form_class = forms.UserCreateForm
    template_name = "accounts/signup.html"

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object, backend=AUTH_BACKEND)
        messages.success(self.request, "Welcome to Star Social!")
        return response

    def get_success_url(self):
        return reverse("posts:all")


class EditProfile(LoginRequiredMixin, generic.UpdateView):
    form_class = forms.UserUpdateForm
    template_name = "accounts/profile_form.html"

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        messages.success(self.request, "Profile updated.")
        return reverse("posts:for_user", kwargs={"username": self.object.username})


class DeleteAccount(LoginRequiredMixin, generic.DeleteView):
    model = get_user_model()
    template_name = "accounts/user_confirm_delete.html"
    success_url = reverse_lazy("home")

    def get_object(self):
        return self.request.user

    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        logout(request)
        user.delete()
        messages.success(request, "Your account has been deleted.")
        return redirect(self.success_url)
