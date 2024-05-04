from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse


class LoginRequiredMixin(object):
    """
    Redirects to the login page if the user is not authenticated.
    """

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login') + '?next=' + request.path)
        return super().dispatch(request, *args, **kwargs)


class SuperuserRequiredMixin(object):
    """
    Redirects to the login page if the user is not authenticated or is not a superuser.
    """

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_superuser:
            return HttpResponseRedirect(reverse('login') + '?next=' + request.path)
        return super().dispatch(request, *args, **kwargs)


class PermissionRequiredMixin(object):
    """
    Redirects to the permission denied page if the user does not have the required permission.
    """
    permission_required = None

    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm(self.permission_required):
            return HttpResponseRedirect(reverse('permission_denied_url'))
        return super().dispatch(request, *args, **kwargs)


class SuccessMessageMixin(object):
    """
    Add a success message on successful form submission.
    """
    success_message = None

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.success_message:
            messages.success(self.request, self.success_message)
        return response

    def get_success_message(self, cleaned_data):
        return self.success_message

    def get_success_url(self):
        return reverse('success_url')


class NextUrlMixin(object):
    """
    Mixin that redirects to the next URL after a form submission.
    """
    default_next = '/'

    def get_next_url(self):
        next_url = self.request.GET.get('next') or self.request.POST.get('next')
        return next_url or self.default_next

    def form_valid(self, form):
        response = super().form_valid(form)
        return redirect(self.get_next_url())
