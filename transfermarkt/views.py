from django.shortcuts import render, redirect
from django.utils import timezone
from datetime import timedelta
from .models import Partita, Utente , Squadra , Nazionalita
from .form import RegistrazioneForm
from .form import LoginForm
from .models import Admin



import hashlib





def benvenuto(request):
    return render(request, 'benvenuto.html')




def partite_settimana(request):
    user_email = request.session.get('user_email', '')
    username = ''
    if user_email:
        try:
            utente = Utente.objects.get(email=user_email)
            username = utente.nome
        except Utente.DoesNotExist:
            pass
    oggi = timezone.now()
    fine_settimana = oggi + timedelta(days=7)
    top_campionati = [
        "Serie a",
        "Bundesliga",
        "Premier League",
        "Ligue 1",
        "LaLiga"
    ]
    partite = Partita.objects.filter(
        campionato__nome__in=top_campionati,
        data__range=(oggi, fine_settimana)
    ).order_by('data')[:10]
    return render(request, 'principale.html', {'partite': partite, 'username': username})


def authenticated(email, password):
    return Utente.objects.filter(email=email, password=password).exists()

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        hashed_password = hashlib.md5(password.encode()).hexdigest()
        # print(email," : ", hashed_password)

        if authenticated(email, hashed_password):
            request.session['user_email'] = email
            return redirect('principale')
        else:
            return render(request, 'login.html', {'error_message': "Credenziali errate"})
    else:
        return render(request, 'login.html')

def registrazione(request):
    nazionalita = Nazionalita.objects.all()
    squadre = Squadra.objects.all()
    return render(request, 'registrazione.html', {
        'nazionalita': nazionalita,
        'squadre': squadre
    })

def authenticated_admin(email, password):
    return Admin.objects.filter(email=email, password=password).exists()

def login_admin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        hashed_password = hashlib.md5(password.encode()).hexdigest()
        print(f"Email: {email}, Password: {password}, Hash: {hashed_password}")

        if authenticated_admin(email, hashed_password):
            request.session['admin_email'] = email
            return redirect('principale_admin')
        else:
            print("Login fallito")
            return render(request, 'login_admin.html', {'error_message': "Credenziali errate"})
    else:
        return render(request, 'login_admin.html')


def principale_admin(request):
    if not request.session.get('admin_email'):
        return redirect('login_admin')
    return render(request, 'principale_admin.html')



def Lista_Nazionalita(request):
    nazionalita = Nazionalita.objects.all()
    print (nazionalita)
    return render(request, 'nazionalita.html', {'nazionalita': nazionalita})

def registrazione(request):
    nazionalita = Nazionalita.objects.all()
    squadre = Squadra.objects.all()
    if request.method == 'POST':
        nome = request.POST.get('nome')
        cognome = request.POST.get('cognome')
        email = request.POST.get('email')
        password = request.POST.get('password')
        data_nascita = request.POST.get('data_nascita')
        nazionalita_nome = request.POST.get('nazionalita')
        squadra_nome = request.POST.get('squadra_preferita')

        hashed_password = hashlib.md5(password.encode()).hexdigest()

        # Recupera oggetti collegati
        nazionalita_obj = Nazionalita.objects.get(nome=nazionalita_nome)
        squadra_obj = Squadra.objects.get(nome=squadra_nome) if squadra_nome else None

        # Crea e salva l'utente
        Utente.objects.create(
            nome=nome,
            cognome=cognome,
            email=email,
            password=hashed_password,
            data_nascita=data_nascita,
            nazionalita=nazionalita_obj,
            squadra_preferita=squadra_obj
        )
        return render(request, 'benvenuto.html', {'form': None, 'success': True})

    return render(request, 'registrazione.html', {
        'nazionalita': nazionalita,
        'squadre': squadre
    })


def aggiungi_partita(request):
    if request.method == 'POST':
        squadra_casa = request.POST.get('squadra_casa')
        squadra_ospite = request.POST.get('squadra_ospite')
        campionato = request.POST.get('campionato')
        giornata = request.POST.get('giornata')
        data = request.POST.get('data')
        stadio = request.POST.get('stadio')
        risultato = request.POST.get('risultato')
        gol_casa = request.POST.get('gol_casa')
        gol_ospite = request.POST.get('gol_ospite')

        Partita.objects.create(
            squadra_casa=squadra_casa,
            squadra_ospite=squadra_ospite,
            campionato=campionato,
            giornata=giornata if giornata else None,
            data=data,
            stadio=stadio,
            risultato=risultato,
            gol_casa=gol_casa if gol_casa else None,
            gol_ospite=gol_ospite if gol_ospite else None
        )
        return redirect('principale_admin')
    return redirect('principale_admin')


def logout(request):
    # Clear the user session
    if 'user_email' in request.session:
        del request.session['user_email']
    # Also clear admin session if it exists
    if 'admin_email' in request.session:
        del request.session['admin_email']
    # Redirect to welcome page
    return redirect('benvenuto')
