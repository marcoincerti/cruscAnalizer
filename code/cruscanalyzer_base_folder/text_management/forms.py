from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Row, Column, HTML
from django import forms
from django.urls import reverse_lazy

from text_management.models import Category, Text, UserTextSettings


class InsertTextCrispyForm(forms.Form):
    """
    Form used for inserting a text.
    Form elements:
        - Title
        - Author (optional)
        - Link (optional)
        - Category (optional)
        - Checbox for deleting the short words
        - Text
    """
    helper = FormHelper()
    helper.form_id = 'insert-text-crispy-form'
    helper.form_method = 'POST'
    helper.form_action = reverse_lazy('text_management:text-analysis', kwargs={})
    helper.add_input(Submit('submit', 'Analizza', css_class='btn btn-info'))

    title = forms.CharField(max_length=150, label='Titolo')
    author = forms.CharField(max_length=150, label='Autore', required=False)
    link = forms.URLField(max_length=250, label='Link', required=False)
    category = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label='Nessuna categoria',
                                      label='Categoria', required=False)
    delete_short_words = forms.BooleanField(required=False, label='Applica la tua impostazione per eliminare le parole'
                                                                  ' troppo corte.')
    text = forms.CharField(max_length=5000, widget=forms.Textarea, label='Corpo del testo')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # set style-input class for the dark-theme
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'style-input'
        # set specific classes for the category field
        self.fields['category'].widget.attrs.update({'class': 'selectpicker forms-select'})

        self.helper.layout = Layout(
            Row(
                Column('title', css_class='form-group mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('author', css_class='form-group mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('link', css_class='form-group col-md-8 mb-0'),
                Column('category', css_class='form-group w-auto mb-0'),
                css_class='form-row'
            ),
            Row(
                Row(
                    # Checkbox for deleting words too short (user setting "min_characters").
                    Column('delete_short_words',
                           css_class='form-group col mb-0 delete-short-words custom-control custom-switch ml-3'),
                    # Adds two whitespace to the title of the checkbox and a help icon with a tooltip.
                    HTML('''
                            <span class="help-tooltip complexity-helper-icon" data-target="#complexity-modal" 
                            data-toggle="modal" 
                            title="Le parole con meno caratteri di quelli selezionati verranno eliminate dall'analisi,'''
                         + ''' ma il calcolo della complessità rimarrà invariato.'''
                         + '''\nPuoi cambiare il numero di caratteri nelle tue impostazioni.">
                            <i class="fas fa-info-circle"></i>
                            </span>
                            '''),
                    css_class='form-row'
                ),
                HTML('<a class="settings-link style-link" href="">Apri le impostazioni</a>'),
                css_class='form-row d-flex justify-content-between'
            ),
            Row(
                Column('text', css_class='form-group mb-0'),
                css_class='form-row'
            ),
        )


class UpdateTextCrispyForm(forms.ModelForm):
    """
    Form used for updating a text.
    Form elements:
        - Title
        - Author (optional)
        - Link (optional)
        - Category (optional)
    """
    helper = FormHelper()
    helper.form_id = 'update-text-crispy-form'
    helper.form_method = 'POST'
    helper.add_input(Submit('submit', 'Salva', css_class='btn btn-success'))
    helper.add_input(Submit('cancel', 'Annulla', css_class='btn btn-secondary'))

    class Meta:
        model = Text
        fields = ('title', 'author', 'link', 'category')
        labels = {
            'title': 'Titolo',
            'author': 'Autore',
            'link': 'Link',
            'category': 'Categoria'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # set style-input class for the dark-theme
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'style-input'
        self.fields['category'].widget.attrs.update({'class': 'selectpicker forms-select'})

        self.helper.layout = Layout(
            Row(
                Column('title', css_class='form-group mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('author', css_class='form-group mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('link', css_class='form-group col-md-8 mb-0'),
                Column('category', css_class='form-group w-auto mb-0'),
                css_class='form-row'
            ),
        )


class UpdateBlacklistCrispyForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_id = 'update-blacklist-form'
    helper.form_method = 'POST'
    helper.add_input(Submit('submit', 'Salva', css_class='btn btn-success'))

    class Meta:
        model = UserTextSettings
        fields = ('blacklist_string',)
        # widgets = {'blacklist_string': forms.HiddenInput()}
