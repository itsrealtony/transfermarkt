# transfermarkt/admin.py
from django.contrib import admin
from .models import Nazionalita, Campionato, Squadra, Giocatore, Utente, Giornata, Partita, Admin

admin.site.register(Nazionalita)
admin.site.register(Campionato)
admin.site.register(Squadra)
admin.site.register(Giocatore)
admin.site.register(Utente)
admin.site.register(Giornata)
admin.site.register(Partita)
admin.site.register(Admin)