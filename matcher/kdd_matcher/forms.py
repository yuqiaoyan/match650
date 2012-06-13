from django import forms

class QueryForm(forms.Form):
    name=forms.CharField(help_text='Your name please...')
    interest = forms.CharField(help_text='e.g. Information Retrieval...')
    affiliation = forms.CharField(label='University / Affiliation',
                                    required=False,
                                    help_text='e.g. University of Michigan...')

class ReviewForm(forms.Form):
    review = forms.CharField()
    resultid = forms.IntegerField(widget=forms.HiddenInput)
    score = forms.IntegerField(widget=forms.HiddenInput)
