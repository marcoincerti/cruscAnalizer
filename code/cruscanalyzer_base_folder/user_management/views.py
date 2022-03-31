from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import FormView
from django.views.generic import CreateView
from django.views.generic.base import View, TemplateView

from cruscanalyzer.views import BasicView
from lib.text_statistics import get_ordered_words_frequencies
from user_management.forms import UpdateUserForm
from text_management.models import Text
from user_management.forms import RegistrationForm, LoginForm


class CreateUserView(CreateView):
    """
    View with registration form
    """
    form_class = RegistrationForm
    template_name = 'registration/registration_form.html'
    success_url = reverse_lazy('user_management:user-login')


class LoginUserView(LoginView):
    """
    View with login form
    """
    form_class = LoginForm
    template_name = 'registration/login.html'
    success_url = reverse_lazy('home')


class LogoutUserView(LogoutView):
    """
    View for logging out
    """
    template_name = 'registration/logged_out.html'
    success_url = reverse_lazy('user_management:user-login')


class ProfileView(BasicView, TemplateView):
    """
    View for displaying the account of the authenticated user.
    """
    template_name = 'user_management/user_profile.html'
    user_for_profile = None
    texts = None

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        labels = []
        frequency = []
        try:
            self.user_for_profile = get_object_or_404(User, pk=self.request.user.pk)
        except ObjectDoesNotExist:
            raise Http404

        self.texts = Text.objects.filter(user_owner_id=self.request.user.pk)
        return context


class UpdateUserView(BasicView, FormView):
    """
    View for updating the data of the authenticated user account.
    """
    template_name = 'user_management/user_update.html'
    success_url = reverse_lazy('user_management:user')

    def post(self, request, *args, **kwargs):
        # Sends the authenticated user to the form in order to update it.
        form = UpdateUserForm(request.POST, request.user)
        # Click on "Cancel" button
        if "cancel" in request.POST:
            return HttpResponseRedirect(reverse_lazy('user_management:user'))
        # Click on "Submit" button
        else:
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse_lazy('user_management:user'))

            context = ({'view': self,
                        'form': form,
                        })
            return super(UpdateUserView, self).render_to_response(context)

    def get(self, request, *args, **kwargs):
        # Populates the form with the authenticated user data.
        form = UpdateUserForm(initial={
            'username': request.user.username,
            'email': request.user.email,
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
        })
        context = ({'view': self,
                    'form': form,
                    })
        return super(UpdateUserView, self).render_to_response(context)


class DeleteUserView(LoginRequiredMixin, View):
    """
    View for deleting the account of the authenticated user.
    Redirects to :view: LoginUserView
    """
    def get(self, request):
        User.objects.get(pk=request.user.pk).delete()
        return HttpResponseRedirect(reverse_lazy('user_management:user-login'))

    def post(self):
        User.objects.get(pk=self.request.user.pk).delete()
        return HttpResponseRedirect(reverse_lazy('user_management:user-login'))
