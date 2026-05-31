from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

from django.urls import reverse, reverse_lazy
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django.views import generic

from groups.models import Group, GroupMember


class CreateGroup(LoginRequiredMixin, generic.CreateView):
    fields = ("name", "description")
    model = Group

    def form_valid(self, form):
        form.instance.owner = self.request.user
        response = super().form_valid(form)
        # The creator owns and joins their own galaxy.
        GroupMember.objects.get_or_create(user=self.request.user, group=self.object)
        messages.success(self.request, "Galaxy launched.")
        return response


class OwnerRequiredMixin(LoginRequiredMixin):
    """Limit edit/delete to the galaxy's owner (404 for everyone else)."""

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)


class UpdateGroup(OwnerRequiredMixin, generic.UpdateView):
    fields = ("name", "description")
    model = Group

    def form_valid(self, form):
        messages.success(self.request, "Galaxy updated.")
        return super().form_valid(form)


class DeleteGroup(OwnerRequiredMixin, generic.DeleteView):
    model = Group
    success_url = reverse_lazy("groups:all")

    def delete(self, *args, **kwargs):
        messages.success(self.request, "Galaxy deleted.")
        return super().delete(*args, **kwargs)


class SingleGroup(generic.DetailView):
    model = Group

class ListGroups(generic.ListView):
    model = Group

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get("q")
        if query:
            queryset = queryset.filter(name__icontains=query)
        return queryset


class JoinGroup(LoginRequiredMixin, generic.RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse("groups:single",kwargs={"slug": self.kwargs.get("slug")})

    def get(self, request, *args, **kwargs):
        group = get_object_or_404(Group,slug=self.kwargs.get("slug"))

        try:
            GroupMember.objects.create(user=self.request.user,group=group)

        except IntegrityError:
            messages.warning(self.request,("Warning, already a member of {}".format(group.name)))

        else:
            messages.success(self.request,"You are now a member of the {} group.".format(group.name))

        return super().get(request, *args, **kwargs)


class LeaveGroup(LoginRequiredMixin, generic.RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse("groups:single",kwargs={"slug": self.kwargs.get("slug")})

    def get(self, request, *args, **kwargs):

        try:

            membership = GroupMember.objects.filter(
                user=self.request.user,
                group__slug=self.kwargs.get("slug")
            ).get()

        except GroupMember.DoesNotExist:
            messages.warning(
                self.request,
                "You can't leave this group because you aren't in it."
            )
        else:
            membership.delete()
            messages.success(
                self.request,
                "You have successfully left this group."
            )
        return super().get(request, *args, **kwargs)
