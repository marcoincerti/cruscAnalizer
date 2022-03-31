from django.test import SimpleTestCase
from django.urls import reverse, resolve
from text_management.views import ViewAnalysis, TextInsert, ViewSavedAnalysis, TextList, TextSearchView, TextDelete, \
    save_analysis, get_translate_data, TextUpdate, ViewComparedAnalysis, DashboardView, TextSettingsView


class TestUrlsTextManagement(SimpleTestCase):
    """Test class to check that urls from text-management app retrieve the correct django view"""

    def test_url_text_insert(self):
        url = reverse("text_management:text-insert")
        self.assertEquals(resolve(url).func.view_class, TextInsert)

    def test_url_analysis_is_resolved(self):
        url = reverse('text_management:text-analysis')
        self.assertEquals(resolve(url).func.view_class, ViewAnalysis)

    def test_url_saved_analysis_is_resolved(self):
        url = reverse("text_management:saved-text-analysis", args=[1])
        self.assertEquals(resolve(url).func.view_class, ViewSavedAnalysis)

    def test_url_list_texts_user_is_resolved(self):
        url = reverse("text_management:text-list")
        self.assertEquals(resolve(url).func.view_class, TextList)

    def test_url_search_is_resolved(self):
        url = reverse("text_management:text-search")
        self.assertEquals(resolve(url).func.view_class, TextSearchView)

    def test_url_delete_text_is_resolved(self):
        url = reverse("text_management:text-delete", args=[1])
        self.assertEquals(resolve(url).func.view_class, TextDelete)

    def test_url_update_text_is_resolved(self):
        url = reverse("text_management:text-update", args=[1])
        self.assertEquals(resolve(url).func.view_class, TextUpdate)

    def test_url_compare_text_is_resolved(self):
        url = reverse("text_management:compare-text-analysis", kwargs={'first_pk': 1, 'second_pk': 2})
        self.assertEquals(resolve(url).func.view_class, ViewComparedAnalysis)

    def test_url_dashboard(self):
        url = reverse("text_management:dashboard")
        self.assertEquals(resolve(url).func.view_class, DashboardView)

    def test_url_user_text_settings(self):
        url = reverse("text_management:text-settings")
        self.assertEquals(resolve(url).func.view_class, TextSettingsView)


class TestUrlsAjaxTextManagement(SimpleTestCase):
    """ Test class to check that urls from text-management app retrieve the correct django view
    implemented with some Ajax function """
    def test_url_save_text_function_is_resolved(self):
        url = reverse("text_management:save-text-function")
        self.assertEquals(resolve(url).func, save_analysis)

    def test_url_translate_data_function_is_resolved(self):
        url = reverse("text_management:translate-word")
        self.assertEquals(resolve(url).func, get_translate_data)


