from django.views.generic import (
    CreateView,
    DetailView,
    UpdateView,
    DeleteView,
    ListView
)
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin
)
from django.urls import reverse_lazy
from accounts.models import Role
from .models import Status, Priority, Issue


class IssueCreateView(LoginRequiredMixin, CreateView):
    model = Issue
    template_name = "issues/new.html"
    fields = [
        "summary", "description",
        "priority", "assignee"
    ]

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.status = Status.objects.get("To Do")
        return super().form_valid(form)


class IssueDetailView(LoginRequiredMixin, DetailView):
    model = Issue
    template_name = "issues/detail.html"


class IssueUpdateView(
    LoginRequiredMixin, 
    UserPassesTestMixin,
    UpdateView):
    model = Issue
    template_name = "issues/edit.html"
    fields = [
        "summary", "description",
        "priority", "status",
        "assignee"
    ]

    def test_func(self):
        issue = self.get_object()
        product_owner = Role.objects.get("product owner")
        return (
            issue.author == self.request.user 
            or self.request.user.role == product_owner
        )


class IssueDeleteView(
    LoginRequiredMixin,
    UserPassesTestMixin, 
    DeleteView):
    model = Issue
    template_name = "issues/delete.html"
    success_url = reverse_lazy("list")

    def test_func(self):
        issue = self.get_object()
        product_owner = Role.objects.get("product owner")
        return (
            issue.author == self.request.user 
            or self.request.user.role == product_owner
        )



class IssueListView(LoginRequiredMixin, ListView):
    model = Issue
    template_name = "issues/list.html"

    def get_context_data(self, **kwargs):
        context = super().get.context_data(**kwargs)
        to_do = Status.objects.get("To Do")
        in_prog = Status.objects.get("In Progess")
        done = Status.objects.get("Done")
        context["to_do_list"] = Issue.objects.filter(
            status=to_do
        ).order_by("priority").reverse()
        context["in_prog_list"] = Issue.objects.filter(
            status=in_prog
        ).order_by("priority").reverse()
        context["done_list"] = Issue.objects.filter(
            status=done
        ).order_by("priority").reverse()
        return context
