from django.db import models

class Nazionalita(models.Model):
    nome = models.CharField(max_length=100, primary_key=True)


class Campionato(models.Model):
    nome = models.CharField(max_length=100, primary_key=True)
    nazionalita = models.ForeignKey(Nazionalita, on_delete=models.CASCADE,
                                    related_name='campionati')

class Squadra(models.Model):
    nome = models.CharField(max_length=100, primary_key=True)
    campionato = models.ForeignKey(Campionato, on_delete=models.CASCADE,
                                   related_name='squadre')
    data_fondazione = models.DateField(null=True)
    stadio = models.CharField(max_length=100, null=True)
    capacita_stadio = models.IntegerField(null=True)
    citta = models.CharField(max_length=100, null=True)

class Giocatore(models.Model):
    id = models.CharField(primary_key=True)
    nome = models.CharField(max_length=100)
    cognome = models.CharField(max_length=100)
    data_nascita = models.DateField(null=True)
    nazionalita = models.ForeignKey(Nazionalita, on_delete=models.CASCADE, related_name='giocatori')
    squadra = models.ForeignKey(Squadra, on_delete=models.CASCADE, related_name='giocatori', null=True, blank=True)
    valore_mercato = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    ruolo = models.CharField(max_length=100, null=True)

class Utente(models.Model):
    nome = models.CharField(max_length=100)
    cognome = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, primary_key=True, unique=True)
    password = models.CharField(max_length=100)
    data_nascita = models.DateField(null=True)
    nazionalita = models.ForeignKey(Nazionalita, on_delete=models.CASCADE, related_name='utenti')
    squadra_preferita = models.ForeignKey(Squadra, on_delete=models.CASCADE, related_name='utenti', null=True, blank=True)

class Partita(models.Model):
    id = models.AutoField(primary_key=True)
    squadra_casa = models.ForeignKey(Squadra, on_delete=models.CASCADE, related_name='partite_casa')
    squadra_ospite = models.ForeignKey(Squadra, on_delete=models.CASCADE, related_name='partite_ospite')
    campionato = models.ForeignKey(Campionato, on_delete=models.CASCADE, related_name='partite')
    data = models.DateTimeField()
    stadio = models.CharField(max_length=100)
    gol_casa = models.IntegerField(null=True, blank=True)
    gol_ospite = models.IntegerField(null=True, blank=True)

