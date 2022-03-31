from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from text_management.models import Text, Category


class BasicView(LoginRequiredMixin):
    """
    View for getting the categories from the db.

    :param categories: the query set that contains all the categories of the app
    """
    categories = Category.objects.all()


class HomePageView(BasicView, TemplateView):
    """
    Home view of the application, showing the last 5 texts insterted and the first 5 most complex texts.
    """
    template_name = 'homepage.html'
    recent_text_list = None
    complex_text_list = None

    def get_context_data(self, **kwargs):
        """
        Searches in the DB the last 5 texts inserted and the first 5 most complex texts.

        :param kwargs:
        :return: Context to populate the template with
        """
        context = super(HomePageView, self).get_context_data(**kwargs)
        self.recent_text_list = Text.objects.all()[:5]
        self.complex_text_list = Text.objects.all().order_by('-complexity')[:5]

        return context


class UserProfileView(BasicView, TemplateView):
    """
    View for displaying a user profile.
    """
    user_for_profile = None
    object_list = None
    template_name = 'user_info.html'

    def get_context_data(self, **kwargs):
        """
        Searches in the DB the selected users and his texts.

        :param kwargs: Used to get the pk of the selected user
        :return: Context to populate the template with
        """
        context = super(UserProfileView, self).get_context_data(**kwargs)
        try:
            self.user_for_profile = get_object_or_404(User, pk=kwargs['pk'])
        except ObjectDoesNotExist:
            raise Http404
        self.object_list = Text.objects.filter(user_owner_id=self.user_for_profile.id)

        return context