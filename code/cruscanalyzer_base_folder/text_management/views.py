import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponseForbidden, HttpResponseRedirect
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST

from django.views.generic import TemplateView, FormView, ListView, DeleteView, UpdateView
from django.urls import reverse_lazy, reverse

from cruscanalyzer.views import BasicView
from lib.text_analysis import ari_complexity_text
from lib.text_statistics import get_avg_complexity
from lib.text_translation import get_languages, translate, detect_language
from text_management.forms import InsertTextCrispyForm, UpdateTextCrispyForm
from text_management.models import Text, Analysis, Category, UserTextSettings


class TextInsert(BasicView, FormView):
    """
    View for inserting the text.

    Contains a :form: InsertCrispyForm.
    """
    template_name = 'text_management/text_insert.html'
    form_class = InsertTextCrispyForm

    def form_valid(self, form):
        return super().form_valid(form)


class BaseViewForAnalysis(BasicView, TemplateView):
    """
    Base View for analyzing a text.

    Used for both :view: ViewAnalysis and :view: ViewSavedAnalysis.
    """
    template_name = 'text_management/single_text_analysis.html'
    text_inserted = None
    # Variable used to store the google translate API languages.
    languages = None


class ViewAnalysis(BaseViewForAnalysis):
    """
    View for displaying the analysis of an inserted text.

    Accessible only through POST method, receives the data of a text and performs all the analysis operations.
    """

    def post(self, request):
        """
        Creates the context with the info of the text received through POST.

        Usually, the data received are passed from the form contained in :view: TextInsert.

        :param request: Used to get the data of the text inserted to analyze
        :return: Context used to populate the template
        """
        # Gets the text inserted from the fields of the insert form.
        self.text_inserted = Text(title=self.request.POST.get('title', ''),
                                  author=self.request.POST.get('author', ''),
                                  link=self.request.POST.get('link', ''),
                                  category=None if self.request.POST.get('category', None) == ''
                                  else Category.objects.get(pk=self.request.POST.get('category', None)),
                                  complexity=ari_complexity_text(self.request.POST.get('text', '')),
                                  )
        self.text_inserted.content = self.request.POST.get('text', '')
        # Gets the checkbox value for deleting short words.
        delete_short_words = True if self.request.POST.get('delete_short_words', False) == 'on' else False
        if delete_short_words:  # Deletes from the text analysis the words that are too short for the user.
            self.text_inserted.remove_short_words_from_analysis(request.user.user_text_settings.min_characters)
        self.languages = get_languages()  # Retrieving list of all languages supported by google translate

        context = ({'view': self,
                    'user': request.user,
                    })
        return super(TemplateView, self).render_to_response(context)


class ViewSavedAnalysis(BaseViewForAnalysis):
    """
    View for displaying a saved analysis.
    """

    def get_context_data(self, **kwargs):
        """
        Searches in the DB the selected text and send the context to the template.

        :param kwargs: Used to get the pk of the selected text
        :return: Context to populate the template with
        """
        context = super(ViewSavedAnalysis, self).get_context_data(**kwargs)
        self.text_inserted = Text.objects.get(pk=self.kwargs['pk'])  # Gets the pk of the selected Text from the URL
        self.languages = get_languages()  # Retrieving list of all languages
        return context


class TextList(BasicView, ListView):
    """
    View for displaying user's list of saved text analysis.
    """
    model = Text
    template_name = 'text_management/user_text_list.html'

    def get_queryset(self):
        """
        Filtrates the metadata of texts in the database owned by the current user using his pk.

        :return: Metadata list of texts of the current user.
        """
        texts = Text.objects.filter(user_owner_id=self.request.user.pk)
        texts.compare_url = False  # each text item in the list must not return the compare page
        for t in texts:
            t.url = 'text_management:saved-text-analysis'
            t.url_params = t.pk
        return texts


class TextDelete(BasicView, DeleteView):
    """
    View for deleting a saved text analysis.
    """
    model = Text
    template_name = 'text_management/text_delete.html'

    success_url = reverse_lazy('text_management:text-list')

    def dispatch(self, request, *args, **kwargs):
        """Checks if user authenticated is owner of the text analysis"""
        if request.user != self.get_object().user_owner:
            # Block requests that attempt to provide their own foo value
            return HttpResponseForbidden()
        # now process dispatch as it otherwise normally would
        return super().dispatch(request, *args, **kwargs)


class TextUpdate(BasicView, UpdateView):
    """
    View for updating the metadata of a saved text analysis.
    """
    model = Text
    form_class = UpdateTextCrispyForm
    template_name = 'text_management/text_update.html'

    def post(self, request, *args, **kwargs):
        """Add 'Cancel' button redirect."""
        if "cancel" in request.POST:
            # url = reverse('text_management:text-list')
            url = reverse_lazy('text_management:saved-text-analysis', kwargs={'pk': self.kwargs['pk']})
            return HttpResponseRedirect(url)
        else:
            return super(TextUpdate, self).post(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        """Checks if user authenticated is owner of the text analysis"""
        if request.user != self.get_object().user_owner:
            # Block requests that attempt to provide their own foo value
            return HttpResponseForbidden()
        # now process dispatch as it otherwise normally would
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('text_management:saved-text-analysis', kwargs={'pk': self.object.pk})


class TextSearchView(BasicView, ListView):
    """
    View for displaying list of results from data searched.
    """
    model = Text
    template_name = None
    context_object_name = 'all_search_results'
    result_users = None  # Used only to show also the list of users.

    def get_queryset(self):
        """
        Query to the database return the results

        Gets the data to search for from the GET request.
        Combine the data and queries the database

        :return: Texts matching the data searched.
        """
        first_text_pk = None
        query = self.request.GET.get('search')

        if self.request.is_ajax():
            """ 
            If the request is ajax, so the result must be included in the compare modal:
                - different template name (one doesn't extends base.html, so it can be included in a complete page)
                - necessary retrieve the first text primary key for the compare
                - categories must be retrieved in different way
            """
            self.template_name = 'text_management/base/base_search_text_list.html'
            first_text_pk = self.request.GET.get('first-text-pk')
            value_category_string = self.request.GET.get('category').replace('[', '').replace(']', '')
            value_category = value_category_string.split(',')
        else:
            self.template_name = 'text_management/search_list.html'
            value_category = self.request.GET.getlist('category')
            # Searches all the app users, excluding the authenticated user and the superusers (like "admin").
            self.result_users = (User.objects.filter(username__icontains=query) |
                                 User.objects.filter(first_name__icontains=query) |
                                 User.objects.filter(last_name__icontains=query)) \
                .exclude(pk=self.request.user.pk).exclude(is_superuser=True) \
                if query else User.objects.all().exclude(pk=self.request.user.pk).exclude(is_superuser=True)
            for user in self.result_users:
                user.avg_complexity = get_avg_complexity(Text.objects.filter(user_owner_id=user.pk))

        if query:  # A query is present inside the searchbar
            if "0" in value_category:  # No particular category selected
                result_texts = (Text.objects.filter(title__icontains=query) | Text.objects.filter(
                    author__icontains=query) |
                                Text.objects.filter(link__istartswith=query))
            else:  # Filters also with the selected categories
                result_texts = (Text.objects.filter(title__icontains=query) | Text.objects.filter(
                    author__icontains=query) |
                                Text.objects.filter(link__istartswith=query)) & \
                               Text.objects.filter(category_id__in=value_category)

        else:  # No query inside searchbar, searches all texts
            if "0" not in value_category:  # No particular category selected, searches all texts
                result_texts = Text.objects.filter(category_id__in=value_category)
            else:  # Searches all texts of the selected categories
                result_texts = Text.objects.all()

        if result_texts:
            if self.request.is_ajax():
                """
                If the request is ajax, so the result must be included in the compare modal:
                    - excluded the text with same primary key of first text (first_text_pk), if present
                    - compare_url must be True
                    - save the first_text_pk in the result
                """
                result_texts = result_texts.exclude(
                    pk=int(first_text_pk))  # excluding same text we are viewing if showing compare search results
                result_texts.compare_url = True  # each text item in the list must return the compare page
                result_texts.first_pk = first_text_pk
            else:
                result_texts.compare_url = False  # each text item in the list must not return the compare page

        if self.result_users:
            for user in self.result_users:  # Adds the number of texts owned by each user.
                user.text_counter = Text.objects.filter(user_owner_id=user.pk).count()

        return result_texts  # Returns the texts found to the template as 'object_list'

    def get_context_data(self, **kwargs):
        context = super(TextSearchView, self).get_context_data(**kwargs)
        context['users_list'] = self.result_users  # Passes the users found to the template
        return context


@login_required
@require_POST
@csrf_protect
def save_analysis(request):
    """
    Function call from ajax request for saving ana analysis.

    Retrieves data attributes from request and use them for saving the metadata of the text and his analysis.
    Accessible only with POST request.

    :param request: Ajax request data
    :returns: Bool indicating if text has been saved
    """
    if request.method == "POST":
        text_to_save = Text(user_owner=request.user,
                            title=request.POST.get('text_to_save[title]'),
                            author=request.POST.get('text_to_save[author]'),
                            link=request.POST.get('text_to_save[link]'),
                            category=None if request.POST.get('text_to_save[category]', None) == '' else
                            Category.objects.get(pk=request.POST.get('text_to_save[category]', None)),
                            complexity=request.POST.get('text_to_save[complexity]'),
                            )
        text_to_save.save()  # Save the Text

        key_analysis = 'text_to_save[analysis]'
        """ 
        Can't use text_to_save.analysis because analysis not stored in DB and text_to_save.content = '', creating local
        variable used to store the analysis got from POST.
        """
        analysis = {key[len(key_analysis) + 1: -1]: request.POST.get(key) for key in request.POST
                    if key.startswith(key_analysis)}
        for word, frequency in analysis.items():
            word_frequency = Analysis(text=text_to_save,
                                      word=word,
                                      frequency=frequency)
            word_frequency.save()  # Save each word with his frequency
        data = {
            'text_saved': True
        }
        return JsonResponse(data)


@login_required
def get_translate_data(request):
    """
    Function call from ajax request for translation.

    Retrieves data attributes of request and use them for translate a word.
    Accessible only with GET request.

    :param request: ajax request data
    :return: translated word
    :return: language source if detected
    """
    if request.method == "GET":
        word = request.GET.get('original_word')
        dest_language = request.GET.get('dest_language')
        detect_language_bool = request.GET.get('detect_language')

        if json.loads(detect_language_bool.lower()):
            source_language = detect_language(word)
            if source_language == 'en':
                dest_language = 'it'
        else:
            source_language = request.GET.get('source_language')

        translated_word = translate(word, source_language, dest_language)

        if detect_language_bool:
            data = {'translated_word': translated_word,
                    'language_source': source_language}
        else:
            data = {'translated_word': translated_word}

        return JsonResponse(data)


class ViewComparedAnalysis(BaseViewForAnalysis):
    """
    View for comparing two selected Text analyzes.
    """
    template_name = 'text_management/compare_text_analysis.html'
    first_text = None
    second_text = None

    def get_context_data(self, **kwargs):
        """
        Searches in the DB the 2 selected texts and send the context updated to the template.

        :param kwargs: Used to get the pk of the two selected texts
        :return: Context to populate the template with
        """
        context = super(ViewComparedAnalysis, self).get_context_data(**kwargs)
        self.first_text = Text.objects.get(
            pk=self.kwargs['first_pk'])  # Gets the pk of the first selected Text from the URL
        self.second_text = Text.objects.get(
            pk=self.kwargs['second_pk'])  # Gets the pk of the second selected Text from the URL
        self.languages = get_languages()  # Retrieving list of all languages
        return context


class TextSettingsView(BasicView, TemplateView):
    """
    View for displaying and saving text settings.
    """
    template_name = 'text_management/text_settings.html'

    def get(self, request, *args, **kwargs):
        context = ({'view': self})
        return super(TextSettingsView, self).render_to_response(context)

    def post(self, request, **kwargs):
        """
        Retrieve the POST data and save to database
        :return: Redirects to :view: ProfileView
        """
        blacklist = self.request.POST.getlist('black-word')
        min_characters = self.request.POST.get('min-characters')
        blacklist_string = ""
        for black_word in blacklist:
            if black_word:
                blacklist_string += str(black_word).lower() + ";"

        blacklist_string = blacklist_string[:-1]
        try:
            UserTextSettings.objects.filter(user=request.user).update(blacklist_string=blacklist_string,
                                                                      min_characters=min_characters
                                                                      if int(min_characters) > 0 else 0)
        except:
            UserTextSettings.objects.filter(user=request.user).update(blacklist_string=blacklist_string)

        return HttpResponseRedirect(reverse_lazy('user_management:user'))


class DashboardView(BaseViewForAnalysis):
    """
    View for displaying dashboard with texts statistics as total number of words, all saved words and their
    frequencies...
    """
    object_list = None
    object_users = None
    object_categories = None
    template_name = 'text_management/dashboard_analytics.html'
    context_object_name = 'object_list'

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)

        self.object_list = Text.objects.all()  # Gets all the existing texts
        self.object_users = User.objects.all().exclude(is_superuser=True)  # Gets all users
        self.object_categories = Category.objects.all()  # Gets all categories
        self.languages = get_languages()  # Retrieving list of all languages

        return context
