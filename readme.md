Transfermarkt - Gestione Calciatori e Squadre
Descrizione del Progetto
Transfermarkt è un'applicazione web basata su Django che permette di gestire informazioni su calciatori, squadre, e statistiche calcistiche. L'applicazione mantiene un database aggiornato con i dati dei giocatori, inclusi valori di mercato, statistiche delle partite e informazioni contrattuali.


Caratteristiche Principali
Gestione dettagliata dei profili dei calciatori
Visualizzazione delle statistiche stagionali
Gestione delle squadre e delle rose
Sistema di utenti con ruoli differenziati (Admin e Utente standard)


Tecnologie Utilizzate
Python 3.13
Django
Database SQLite (predefinito)
HTML per il frontend


Struttura del Progetto

transfermarkt
│templates/             # Template HTML
│manage.py              # Script di gestione Django
│
├── transfermarkt/                  
│   ├── migrations/        # Migrazioni database
│   ├── models.py          # Modelli dati (Giocatore, Squadra, ecc.)
│   ├── views.py           # Logica di visualizzazione
│   └── urls.py            # URL routing
│



Installazione e Avvio del Progetto:


1. Clona il repository


git clone https://github.com/itsrealtony/transfermarkt.git
cd transfermarkt

2. Crea e attiva un ambiente virtuale


python -m venv venv
venv\Scripts\activate

3. Installa le dipendenze


pip install -r requirements.txt

4. Applica le migrazioni al database


python manage.py migrate

5. Avvia il server di sviluppo


python manage.py runserver


7. Accedi all'applicazione 

8. Apri il browser e vai su http://127.0.0.1:8000/

9. Creare un utente tramite registrazione o accedere con un account esistente.

