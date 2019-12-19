from django import forms


class SubmitSentenceForm(forms.Form):
    sentence = forms.CharField()


class SupervisedClassificationForm(forms.Form):
    sentence = forms.CharField()
    classification = forms.CharField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['sentence'].disabled = True  # This does not work. It struggles with the validation
        self.fields['sentence'].widget.attrs['readonly'] = True
