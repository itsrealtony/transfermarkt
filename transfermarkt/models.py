from django.db import models

class Nazionalita(models.Model):
    nome = models.CharField(max_length=100, primary_key=True)
    def __str__(self):
        return self.nome


class Campionato(models.Model):
    nome = models.CharField(max_length=100, primary_key=True)
    nazionalita = models.ForeignKey(Nazionalita, on_delete=models.CASCADE,
                                    related_name='campionati')
    def __str__(self):
        return self.nome

class Squadra(models.Model):
    nome = models.CharField(max_length=100, primary_key=True)
    campionato = models.ForeignKey(Campionato, on_delete=models.CASCADE,
                                   related_name='squadre')
    data_fondazione = models.DateField(null=True, blank=True)
    stadio = models.CharField(max_length=100, null=True)
    capacita_stadio = models.IntegerField(null=True)
    citta = models.CharField(max_length=100, null=True)
    def __str__(self):
        return self.nome

class Giocatore(models.Model):
    id = models.CharField(primary_key=True)
    nome = models.CharField(max_length=100)
    cognome = models.CharField(max_length=100)
    data_nascita = models.DateField(null=True)
    nazionalita = models.ForeignKey(Nazionalita, on_delete=models.CASCADE, related_name='giocatori')
    squadra = models.ForeignKey(Squadra, on_delete=models.CASCADE, related_name='giocatori', null=True, blank=True)
    valore_mercato = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    ruolo = models.CharField(max_length=100, null=True)
    gol_fatti = models.IntegerField(null=True, blank=True)
    assist = models.IntegerField(null=True, blank=True)
    presenze = models.IntegerField(null=True, blank=True)
    cartellini_rossi = models.IntegerField(null=True, blank=True)
    cartellini_gialli = models.IntegerField(null=True, blank=True)
    contratto =models.DateField(null=True, blank=True)


class Admin(models.Model):
    nome = models.CharField(max_length=100)
    cognome = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, primary_key=True, unique=True)
    password = models.CharField(max_length=100)

class Utente(models.Model):
    nome = models.CharField(max_length=100)
    cognome = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, primary_key=True, unique=True)
    password = models.CharField(max_length=100)
    data_nascita = models.DateField(null=True)
    nazionalita = models.ForeignKey(Nazionalita, on_delete=models.CASCADE, related_name='utenti')
    squadra_preferita = models.ForeignKey(Squadra, on_delete=models.CASCADE, related_name='utenti', null=True, blank=True)



class Giornata(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    numero = models.IntegerField()
    campionato = models.ForeignKey(Campionato, on_delete=models.CASCADE, related_name='giornate')

    class Meta:
        unique_together = ('numero', 'campionato')

    def __str__(self):
        return f"Giornata {self.numero} - {self.campionato.nome}"




class Partita(models.Model):
    id = models.AutoField(primary_key=True)
    squadra_casa = models.ForeignKey(Squadra, on_delete=models.CASCADE, related_name='partite_casa')
    squadra_ospite = models.ForeignKey(Squadra, on_delete=models.CASCADE, related_name='partite_ospite')
    campionato = models.ForeignKey(Campionato, on_delete=models.CASCADE, related_name='partite')
    giornata = models.ForeignKey(Giornata, on_delete=models.CASCADE, related_name='partite', null=True, blank=True)
    risultato = models.CharField(max_length=10, null=True, blank=True)
    data = models.DateTimeField()
    stadio = models.CharField(max_length=100)
    gol_casa = models.IntegerField(null=True, blank=True)
    gol_ospite = models.IntegerField(null=True, blank=True)




