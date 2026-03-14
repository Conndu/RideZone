from urllib import request
from django import forms
from django.http import HttpResponse
from datetime import datetime, date 
from collections import Counter
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from .models import CustomUser, Motocicleta, Categorie, Marca, Motor, Furnizor, Piesa, Vizualizare, Promotie
import os
import json
import time
import re
import uuid
from .forms import MotocicletaFilterForm, ContactForm, MotocicletaForm, PromotieForm, CustomUserCreationForm, CustomLoginForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail, send_mass_mail, mail_admins
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.db.models import Count
import logging
import locale    
GLOBAL_LOG = []
GLOBAL_PATH_COUNTS = Counter()

logger = logging.getLogger(__name__)

try:
    locale.setlocale(locale.LC_TIME, "ro_RO.UTF-8")
except: 
    locale.setlocale(locale.LC_TIME, "romanian")
def afis_data(parametru=None):
    acum = datetime.now()
    
    if (parametru == "zi"):
        continut = acum.strftime("%A, %d %B %Y")
        titlu = "Data curenta"
    elif (parametru == "ora"):
        continut = acum.strftime("%H:%M:%S")
        titlu = "Ora curenta"
    else: 
        continut = acum.strftime("%A, %d %B %Y, %H:%M:%S")
        titlu = "Data si ora curenta"
        
    html = f"""
            <section>
                <h2> {titlu} </h2>
                <p> {continut}</p>
            </section>
    """
    return html

def index(request):
    return render(request, 'magazin_moto/index.html')
 
def info(request):
    parametru = request.GET.get("data")
    sectiune_data = afis_data(parametru)
    params = request.GET
    params_count = len(params)
    params_names = list(params.keys())
    html_params = "<h2>Sectiunea Parametri</h2>"
    html_params += f"<p>Această pagină a primit <strong>{params_count}</strong> parametri.</p>"
    if params_names:
        html_params += "<p>Numele parametrilor sunt:</p><ul>"
        for name in params_names:
            html_params += f"<li>{name}</li>"
        html_params += "</ul>"
    return HttpResponse(f"""
                        <html>
                        <head><title> Informatii despre server </title></head>
                        <body>
                            <h1>Info</h1>
                            {sectiune_data}
                            <hr>
                            {html_params}
                        </body>
                        </html>
                        """
                        )
 
class Accesare:
    _counter = 0
    def __init__(self, request):
        Accesare._counter += 1
        self.id = Accesare._counter

        self.path = request.path_info + (f"?{request.GET.urlencode()}" if request.GET else "")
        self.timestamp = datetime.now()
        self.method = request.method
        self.params = request.GET.copy()
        self.base_path = request.path_info
def log_view(request): 
    all_logs = GLOBAL_LOG[:] 
    logs_to_display = []
    error_message = None
    context = {} 

    iduri_params = request.GET.getlist('iduri')
    if iduri_params:
        dubluri = request.GET.get('dubluri', 'false').lower() == 'true'
        requested_ids = []
        seen_ids = set()

        for id_group in iduri_params:
            ids = id_group.split(',')
            for id_str in ids:
                try:
                    id_val = int(id_str.strip())
                    if dubluri:
                        requested_ids.append(id_val)
                    elif id_val not in seen_ids:
                        requested_ids.append(id_val)
                        seen_ids.add(id_val)
                except ValueError:
                    error_message = f"ID-ul '{id_str}' nu este valid."
                    
        logs_by_id_map = {entry.id: entry for entry in all_logs}
        for id_val in requested_ids:
            log = logs_by_id_map.get(id_val)
            if log:
                logs_to_display.append(log)
                
    elif 'ultimele' in request.GET:
        try:
            n = int(request.GET.get('ultimele'))
            if n < 0:
                error_message = "Parametrul 'ultimele' nu poate fi negativ."
                n = 0 
            
            k = len(all_logs)
            if n > k:
                logs_to_display = all_logs[:]
                error_message = f"Exista doar {k} accesari fata de {n} accesari cerute"
            else:
                logs_to_display = all_logs[-n:]
        
        except ValueError:
            error_message = "Parametrul 'ultimele' trebuie sa fie un numar intreg."
            logs_to_display = []

    else:
        logs_to_display = all_logs[:]

    accesari_param = request.GET.get('accesari')
    if accesari_param == 'nr':
        context['total_accesses'] = len(GLOBAL_LOG)
    elif accesari_param == 'detalii':
        context['show_details'] = True

    tabel_param = request.GET.get('tabel')
    if tabel_param:
        context['show_table'] = True
        if tabel_param == 'tot':
            context['table_headers'] = ['id', 'path', 'timestamp', 'method', 'params']
        else:
            context['table_headers'] = [h.strip() for h in tabel_param.split(',')]

    if GLOBAL_PATH_COUNTS:
        most_common = GLOBAL_PATH_COUNTS.most_common()
        context['most_accessed'] = most_common[0][0]
        context['least_accessed'] = most_common[-1][0]
    else:
        context['most_accessed'] = None
        context['least_accessed'] = None

    context['logs'] = logs_to_display
    context['error_message'] = error_message

    return render(request, "magazin_moto/log.html", context)


def afis_template(request):
    return render(request,"magazin_moto/exemplu.html",
        {
            "titlu_tab":"Titlu fereastra",
            "titlu_articol":"Titlu afisat",
            "continut_articol":"Continut text"
        }
    )
    
def produse_view(request):
    form = MotocicletaFilterForm(request.GET)
    produse_list = Motocicleta.objects.all()

    if form.is_valid():
        if form.cleaned_data['nume']:
            produse_list = produse_list.filter(model__icontains=form.cleaned_data['nume'])

        if form.cleaned_data['pret_min']:
            produse_list = produse_list.filter(pret__gte=form.cleaned_data['pret_min'])
        if form.cleaned_data['pret_max']:
            produse_list = produse_list.filter(pret__lte=form.cleaned_data['pret_max'])

        if form.cleaned_data['categorie']:
            produse_list = produse_list.filter(categorie=form.cleaned_data['categorie'])

        if form.cleaned_data['doar_noi']:
            produse_list = produse_list.filter(an_fabricatie__gt=2023)

    sort_param = request.GET.get('sort')
    if sort_param == 'a':
        produse_list = produse_list.order_by('pret')
    elif sort_param == 'd':
        produse_list = produse_list.order_by('-pret')

    mesaj_paginare = None
    if request.GET.get('page') and (form.cleaned_data.get('nume') or form.cleaned_data.get('pret_min')):
         mesaj_paginare = "Atenție! Deoarece ați schimbat pagina în timp ce filtrați, este posibil să fi pierdut unele rezultate."

    paginator = Paginator(produse_list, 5) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'produse': page_obj,
        'categorii': Categorie.objects.all(),
        'current_sort': sort_param if sort_param else '',
        'form': form,
        'mesaj_paginare': mesaj_paginare
    }
    return render(request, 'magazin_moto/produse.html', context)

def produs_detail(request, id_motocicleta):
    try:
        produs = get_object_or_404(Motocicleta, id_motocicleta=id_motocicleta)
        if request.user.is_authenticated:
            Vizualizare.objects.create(user=request.user, produs=produs)

            vizualizari_user = Vizualizare.objects.filter(user=request.user).order_by('-data_vizualizare')
            
            if vizualizari_user.count() > 5:
                ids_de_pastrat = list(vizualizari_user.values_list('id', flat=True)[:5])
                Vizualizare.objects.filter(user=request.user).exclude(id__in=ids_de_pastrat).delete()
        return render(request, 'magazin_moto/produs_detail.html', {'produs': produs})

    except Exception as e:
        logger.error(f"Eroare critică la produsul {id_motocicleta}: {str(e)}")

        subiect = f"Eroare Critica la Produsul ID {id_motocicleta}"
        mesaj_text = f"A aparut o eroare: {str(e)}"

        mesaj_html = f"""
            <div style="background-color: red; color: white; padding: 20px; font-family: Arial;">
                <h1 style="margin-top: 0;">ATENȚIE: EROARE SITE!</h1>
                <p><strong>Mesaj eroare:</strong> {str(e)}</p>
                <p>Produs ID vizat: {id_motocicleta}</p>
                <p>User afectat: {request.user}</p>
            </div>
        """

        mail_admins(subiect, mesaj_text, html_message=mesaj_html)
        print("--- MAIL DE EROARE TRIMIS LA ADMINI ---")
        
        return render(request, 'magazin_moto/index.html', {'mesaj_eroare': "Ne pare rău, a apărut o problemă tehnică."})
    

def adauga_motocicleta_view(request):
    mesaj = ""
    if request.method == 'POST':
        form = MotocicletaForm(request.POST, request.FILES)
        if form.is_valid():
            moto = form.save(commit=False)
            pret_achizitie = form.cleaned_data['pret_achizitie']
            adaos = form.cleaned_data['adaos_procent']
            moto.pret = pret_achizitie + (pret_achizitie * adaos / 100)
            moto.data_introducere = date.today()
            moto.save()

            mesaj = f"Motocicleta {moto.model} a fost adăugată cu prețul calculat de {moto.pret} EUR!"
            form = MotocicletaForm()
    else:
        form = MotocicletaForm()
        
    return render(request, 'magazin_moto/add_motocicleta.html', {'form': form, 'mesaj': mesaj})

def categorie_view(request, nume_categorie):
    categorii = Categorie.objects.all()
    categorie_curenta = get_object_or_404(Categorie, nume__iexact=nume_categorie)

    form = MotocicletaFilterForm(request.GET or {'categorie': categorie_curenta})
    
    form.fields['categorie'].widget = forms.HiddenInput()

    
    produse_list = Motocicleta.objects.filter(categorie=categorie_curenta)

    if form.is_valid():
        if form.cleaned_data['nume']:
            produse_list = produse_list.filter(model__icontains=form.cleaned_data['nume'])
        if form.cleaned_data['pret_min']:
            produse_list = produse_list.filter(pret__gte=form.cleaned_data['pret_min'])
        if form.cleaned_data['pret_max']:
            produse_list = produse_list.filter(pret__lte=form.cleaned_data['pret_max'])
            
        input_cat = form.cleaned_data['categorie']
        if input_cat and input_cat != categorie_curenta:
            pass 

    paginator = Paginator(produse_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'produse': page_obj,
        'categorii': categorii,
        'categorie_curenta': categorie_curenta,
        'form': form
    }
    return render(request, 'magazin_moto/produse.html', context)


def contact_view(request):
    mesaj_succes = None
    
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data

            today = date.today()
            dn = cleaned_data['data_nasterii']
            ani = today.year - dn.year - ((today.month, today.day) < (dn.month, dn.day))
            luni = (today.year - dn.year) * 12 + today.month - dn.month
            luni_ramase = luni % 12
            varsta_str = f"{ani} ani și {luni_ramase} luni"
            raw_mesaj = cleaned_data['mesaj']
            proc_mesaj = raw_mesaj.replace('\n', ' ').replace('\r', '')
            proc_mesaj = re.sub(r'\s+', ' ', proc_mesaj)

            def capitalize_match(match):
                return match.group().upper()
            proc_mesaj = re.sub(r'([.?!]\s*)([a-z])', capitalize_match, proc_mesaj)

            is_urgent = False
            tip = cleaned_data['tip_mesaj']
            zile = cleaned_data['zile_asteptare']
            
            limita_urgenta = 0
            if tip in ['review', 'cerere']: limita_urgenta = 4
            elif tip == 'intrebare': limita_urgenta = 2
            
            if zile == limita_urgenta and limita_urgenta > 0:
                is_urgent = True

            data_to_save = {
                'nume': cleaned_data['nume'],
                'prenume': cleaned_data['prenume'],
                'cnp': cleaned_data['cnp'],
                'varsta_calculata': varsta_str,
                'email': cleaned_data['email'],
                'tip_mesaj': tip,
                'subiect': cleaned_data['subiect'],
                'mesaj': proc_mesaj,
                'zile_asteptare': zile,
                'urgent': is_urgent,
                'ip_address': request.META.get('REMOTE_ADDR'),
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            folder_path = os.path.join(os.path.dirname(__file__), 'Mesaje')
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)

            ts = int(time.time())
            filename = f"mesaj_{ts}"
            if is_urgent:
                filename += "_urgent"
            filename += ".json"
            
            full_path = os.path.join(folder_path, filename)
            
            with open(full_path, 'w') as f:
                json.dump(data_to_save, f, indent=4)
                
            mesaj_succes = f"Mesajul a fost trimis cu succes! (Salvat ca {filename})"
            form = ContactForm()
            
    else:
        form = ContactForm()
        
    return render(request, 'magazin_moto/contact.html', {'form': form, 'mesaj_succes': mesaj_succes})

def inregistrare_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)

            cod_unic = str(uuid.uuid4())
            user.cod = cod_unic
            user.email_confirmat = False
            user.save()

            subiect = "Confirmare cont RideZone"
            link_confirmare = f"http://127.0.0.1:8000/magazin_moto/confirma_mail/{cod_unic}/"

            html_message = render_to_string('magazin_moto/email_confirmare.html', {
                'nume': user.last_name,
                'prenume': user.first_name,
                'username': user.username,
                'link': link_confirmare
            })
            plain_message = strip_tags(html_message)
            
            send_mail(
                subiect,
                plain_message,
                settings.EMAIL_HOST_USER if hasattr(settings, 'EMAIL_HOST_USER') else 'admin@ridezone.ro',
                [user.email],
                html_message=html_message
            )
            
            return render(request, 'magazin_moto/inregistrare_succes.html')
            
    else:
        form = CustomUserCreationForm()
    return render(request, 'magazin_moto/inregistrare.html', {'form': form})

def login_view(request):
    ip_address = request.META.get('REMOTE_ADDR')

    if request.method == 'POST':
        form = CustomLoginForm(data=request.POST)

        if form.is_valid():
            request.session['failed_login_history'] = []
            
            user = form.get_user()

            if not user.email_confirmat:
                return render(request, 'magazin_moto/login.html', {
                    'form': form, 
                    'error_message': "Te rugăm să confirmi adresa de email înainte de logare!"
                })

            login(request, user)

            if form.cleaned_data['remember_me']:
                request.session.set_expiry(86400)
            else:
                request.session.set_expiry(0)

            request.session['user_localitate'] = user.oras
            
            return redirect('profil')

        else:
            attempts = request.session.get('failed_login_history', [])
            current_time = time.time()
            attempts = [t for t in attempts if current_time - t < 120]
            attempts.append(current_time)
            request.session['failed_login_history'] = attempts
            if len(attempts) >= 3:
                username_suspect = request.POST.get('username', 'necunoscut')

                subiect = "Logari suspecte"
                mesaj_text = f"User: {username_suspect}, IP: {ip_address}"
                mesaj_html = f"""
                    <h1 style='color: red;'>Logari suspecte</h1>
                    <p>Username incercat: <strong>{username_suspect}</strong></p>
                    <p>Adresa IP: <strong>{ip_address}</strong></p>
                    <p>Data: {time.ctime()}</p>
                """

                mail_admins(subiect, mesaj_text, html_message=mesaj_html)
                
                request.session['failed_login_history'] = []
                print("--- ALERTA SECURITATE TRIMISA LA ADMINI ---")

    else:
        form = CustomLoginForm()
        
    return render(request, 'magazin_moto/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('index')

@login_required
def profil_view(request):
    localitate_sess = request.session.get('user_localitate', '-')
    return render(request, 'magazin_moto/profil.html', {'localitate_sess': localitate_sess})

def confirma_mail_view(request, cod):
    try:
        user = CustomUser.objects.get(cod=cod)
        if user.email_confirmat:
            mesaj = "Adresa de email a fost deja confirmată."
        else:
            user.email_confirmat = True
            user.save()
            mesaj = "Email confirmat cu succes! Acum te poți autentifica."
    except CustomUser.DoesNotExist:
        mesaj = "Cod invalid sau expirat."
        
    return render(request, 'magazin_moto/rezultat_confirmare.html', {'mesaj': mesaj})

def promotii_view(request):
    mesaj_info = ""
    
    if request.method == 'POST':
        form = PromotieForm(request.POST)
        if form.is_valid():
            promotie = form.save()
            
            categorii_selectate = form.cleaned_data['categorii_tinta']
            promotie.categorii.set(categorii_selectate)
            datatuple = []
            
            K = 3
            total_mailuri = 0

            for cat in categorii_selectate:
                users_interesati = Vizualizare.objects.filter(produs__categorie=cat)\
                    .values('user', 'user__email')\
                    .annotate(cnt=Count('id'))\
                    .filter(cnt__gte=K)
                
                lista_emailuri = [u['user__email'] for u in users_interesati]
                
                if lista_emailuri:
                    template_name = 'magazin_moto/emails/promo_standard.txt'
                    if 'Sport' in cat.nume:
                        template_name = 'magazin_moto/emails/promo_sport.txt'
                    elif 'Touring' in cat.nume:
                        template_name = 'magazin_moto/emails/promo_touring.txt'

                    context = {
                        'subiect': promotie.subiect,
                        'cod_promo': promotie.cod_promo,
                        'discount': promotie.discount,
                        'data_expirare': promotie.data_expirare,
                    }
                    continut_mail = render_to_string(template_name, context)
                    datatuple.append((
                        promotie.subiect,
                        continut_mail,
                        'oferte@ridezone.ro',
                        lista_emailuri
                    ))
                    total_mailuri += len(lista_emailuri)
            if datatuple:
                send_mass_mail(tuple(datatuple), fail_silently=False)
                mesaj_info = f"Promoția a fost creată și trimisă la {total_mailuri} utilizatori interesati!"
            else:
                mesaj_info = "Promoția a fost creată, dar nimeni nu s-a calificat pentru ea (prea puține vizualizări)."
                
            form = PromotieForm()
    else:
        form = PromotieForm()
        
    return render(request, 'magazin_moto/promotii.html', {'form': form, 'mesaj_info': mesaj_info})