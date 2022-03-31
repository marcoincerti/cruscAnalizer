from django.urls import path

from text_management import views
from text_management.views import DashboardView

app_name = 'text_management'

urlpatterns = [
    path('text/analysis', views.ViewAnalysis.as_view(), name='text-analysis'),
    path('text/insert', views.TextInsert.as_view(), name='text-insert'),
    path('text/<int:pk>/analysis', views.ViewSavedAnalysis.as_view(), name='saved-text-analysis'),
    path('analysis/<int:first_pk>/<int:second_pk>/compare', views.ViewComparedAnalysis.as_view(),
         name='compare-text-analysis'),
    path('text/list', views.TextList.as_view(), name='text-list'),
    path('text/search', views.TextSearchView.as_view(), name='text-search'),
    path('text/<int:pk>/delete', views.TextDelete.as_view(), name='text-delete'),
    path('text/<int:pk>/update', views.TextUpdate.as_view(), name='text-update'),
    path('text/save', views.save_analysis, name='save-text-function'),
    path('text/settings', views.TextSettingsView.as_view(), name='text-settings'),
    path('text/translation', views.get_translate_data, name='translate-word'),
    path('dashboard', DashboardView.as_view(), name='dashboard'),
]
