from django.shortcuts import render, redirect
from django.utils import timezone
from datetime import timedelta
from .models import Partita, Utente, Squadra, Nazionalita, Classifica, Giocatore
from .form import RegistrazioneForm
from .form import LoginForm
from .models import Admin
from .models import Campionato, Giornata



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


    campionato_selezionato = request.GET.get('campionato', '')
    giornata_selezionata = request.GET.get('giornata', '')


    if giornata_selezionata and giornata_selezionata.isdigit():
        giornata_selezionata = int(giornata_selezionata)
    else:
        giornata_selezionata = None

    oggi = timezone.now()
    fine_settimana = oggi + timedelta(days=7)
    top_campionati = [
        "Serie A",
        "Bundesliga",
        "Premier League",
        "Ligue 1",
        "LaLiga"
    ]



    campionati = Campionato.objects.filter(nome__in=top_campionati)


    giornate_numeri = Giornata.objects.filter(campionato__nome__in=top_campionati).values_list('numero', flat=True)
    giornate_numeri = sorted(set(giornate_numeri))
    giornate = [{'numero': numero} for numero in giornate_numeri]


    partite_query = Partita.objects.filter(
        campionato__nome__in=top_campionati
    )


    if campionato_selezionato:
        partite_query = partite_query.filter(campionato__nome=campionato_selezionato)

    if giornata_selezionata:
        partite_query = partite_query.filter(giornata__numero=giornata_selezionata)
    else:

        partite_query = partite_query.filter(data__range=(oggi, fine_settimana))


    partite = partite_query.order_by('data')[:10]

    # Query per la classifica
    if campionato_selezionato:
        classifica = Classifica.objects.filter(campionato__nome=campionato_selezionato).order_by('posizione')
    else:
        # Se nessun campionato è selezionato, mostra la classifica del primo campionato disponibile
        classifica = Classifica.objects.filter(campionato__nome__in=top_campionati).order_by('campionato__nome', 'posizione')

    return render(request, 'principale.html', {
        'partite': partite, 
        'username': username,
        'campionati': campionati,
        'giornate': giornate,
        'campionato_selezionato': campionato_selezionato,
        'giornata_selezionata': giornata_selezionata,
        'classifica': classifica
    })


def authenticated(email, password):
    return Utente.objects.filter(email=email, password=password).exists()

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
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
        hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
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

    # Recupera tutti i campionati per il menu a tendina
    campionati = Campionato.objects.all().order_by('nome')

    # Ottieni il campionato selezionato dalla richiesta GET
    campionato_selezionato = request.GET.get('campionato')

    # Se non è stato selezionato un campionato e ci sono campionati disponibili,
    # seleziona il primo come default
    if not campionato_selezionato and campionati.exists():
        campionato_selezionato = campionati.first().nome

    # Recupera le squadre del campionato selezionato
    squadre = []
    if campionato_selezionato:
        squadre = Squadra.objects.filter(campionato__nome=campionato_selezionato).order_by('nome')

    return render(request, 'principale_admin.html', {
        'campionati': campionati,
        'squadre': squadre,
        'campionato_selezionato': campionato_selezionato
    })



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

        hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()


        nazionalita_obj = Nazionalita.objects.get(nome=nazionalita_nome)
        squadra_obj = Squadra.objects.get(nome=squadra_nome) if squadra_nome else None


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

        squadra_casa_nome = request.POST.get('squadra_casa')
        squadra_ospite_nome = request.POST.get('squadra_ospite')
        campionato_nome = request.POST.get('campionato')
        giornata_numero = request.POST.get('giornata')
        data = request.POST.get('data')
        stadio = request.POST.get('stadio')
        risultato = request.POST.get('risultato')
        gol_casa = request.POST.get('gol_casa')
        gol_ospite = request.POST.get('gol_ospite')


        try:
            squadra_casa = Squadra.objects.get(nome=squadra_casa_nome)
            squadra_ospite = Squadra.objects.get(nome=squadra_ospite_nome)
            campionato = Campionato.objects.get(nome=campionato_nome)


            giornata = None
            if giornata_numero:
                try:

                    giornata = Giornata.objects.get(numero=giornata_numero, campionato=campionato)
                except Giornata.DoesNotExist:

                    pass


            Partita.objects.create(
                squadra_casa=squadra_casa,
                squadra_ospite=squadra_ospite,
                campionato=campionato,
                giornata=giornata,
                data=data,
                stadio=stadio,
                risultato=risultato,
                gol_casa=gol_casa if gol_casa else None,
                gol_ospite=gol_ospite if gol_ospite else None
            )

            return redirect('principale_admin')
        except (Squadra.DoesNotExist, Campionato.DoesNotExist) as e:

            return redirect('principale_admin')

    return redirect('principale_admin')


def area_tifoso(request):
    user_email = request.session.get('user_email', '')
    username = ''
    squadra_preferita = None
    classifica = []
    giocatori = []

    # prendi i parametri di ordinamento dalla richiesta
    sort_by = request.GET.get('sort_by', '')
    sort_order = request.GET.get('sort_order', 'desc')


    if not sort_by:
        sort_by = 'valore_mercato'

    if not user_email:
        return redirect('login')

    try:
        utente = Utente.objects.get(email=user_email)
        username = utente.nome
        squadra_preferita = utente.squadra_preferita

        if squadra_preferita:
            # prendi il campionato della squadra preferita
            campionato = squadra_preferita.campionato

            # prendi la classifica del campionato
            classifica = Classifica.objects.filter(campionato=campionato).order_by('posizione')

            # prendi giocatori dalla squadra
            giocatori = Giocatore.objects.filter(squadra=squadra_preferita)



            # organizza i giocatori in base al parametro di ordinamento
            if sort_by == 'valore_mercato':
                # organizza in base al valore di mercato
                giocatori = sorted(giocatori, key=lambda g: g.valore_mercato or 0, reverse=(sort_order == 'desc'))
            elif sort_by == 'presenze':
                # organizza in base alle presenze
                giocatori = sorted(giocatori, key=lambda g: g.presenze or 0, reverse=(sort_order == 'desc'))
            elif sort_by == 'gol_fatti':
                # organizza in base ai gol fatti
                giocatori = sorted(giocatori, key=lambda g: g.gol_fatti or 0, reverse=(sort_order == 'desc'))
            elif sort_by == 'assist':
                # organizza in base agli assist
                giocatori = sorted(giocatori, key=lambda g: g.assist or 0, reverse=(sort_order == 'desc'))
            elif sort_by == 'cartellini_gialli':
                # organizza in base ai cartellini gialli
                giocatori = sorted(giocatori, key=lambda g: g.cartellini_gialli or 0, reverse=(sort_order == 'desc'))
            elif sort_by == 'cartellini_rossi':
                # organizza in base ai cartellini rossi
                giocatori = sorted(giocatori, key=lambda g: g.cartellini_rossi or 0, reverse=(sort_order == 'desc'))

    except Utente.DoesNotExist:
        return redirect('login')

    return render(request, 'area_tifoso.html', {
        'username': username,
        'squadra_preferita': squadra_preferita,
        'classifica': classifica,
        'giocatori': giocatori,
        'sort_by': sort_by,
        'sort_order': sort_order
    })

def logout(request):

    if 'user_email' in request.session:
        del request.session['user_email']

    if 'admin_email' in request.session:
        del request.session['admin_email']

    return redirect('benvenuto')
