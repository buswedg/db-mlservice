from django import forms


class ButtonHolderMixin(object):
    """
    A mixin for Django form classes that allows setting a button for the form.
    """
    button = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.button is not None:
            self.fields['submit'] = forms.CharField(widget=forms.HiddenInput(), initial=self.button)

    def render_button(self):
        return '<button type="submit">{}</button>'.format(self.button)
