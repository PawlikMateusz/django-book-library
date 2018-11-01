from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(label='Imię')
    email = forms.EmailField(label='E-mail')
    message = forms.CharField(label='Wiadomość', widget=forms.Textarea())


class CommentForm(forms.Form):
    text = forms.CharField(label='Dodaj komentarz:', widget=forms.Textarea(
        attrs={'rows': 4, 'cols': 15}))
