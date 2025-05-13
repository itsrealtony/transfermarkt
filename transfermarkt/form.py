from django import forms
from .models import Nazionalita, Squadra, Utente

class LoginForm(forms.Form):
    nazionalita = forms.ChoiceField(choices=[])
    squadra_preferita = forms.ChoiceField(choices=[])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nazionalita'].choices = [
            (n.nome, n.nome) for n in Nazionalita.objects.all()
        ]
        self.fields['squadra_preferita'].choices = [
            (s.nome, s.nome) for s in Squadra.objects.all()
        ]

class RegistrazioneForm:
    class Meta:
        model = Utente
        fields = ['nome', 'cognome', 'email', 'password', 'data_nascita', 'nazionalita', 'squadra_preferita']
        widgets = {
            'password': forms.PasswordInput(),
            'data_nascita': forms.DateInput(attrs={'type': 'date'}),
        }