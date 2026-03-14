from django import forms
from .models import Categorie, Motocicleta, Promotie
import re
from datetime import date, datetime
from django import forms
from django.core.exceptions import ValidationError 
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser
from django.core.mail import mail_admins

class MotocicletaFilterForm(forms.Form):
    nume = forms.CharField(
        required=False, 
        label="Nume conține",
        widget=forms.TextInput(attrs={'placeholder': 'Ex: Yamaha', 'class': 'form-control'})
    )
    
    pret_min = forms.DecimalField(
        required=False, 
        min_value=0, 
        label="Preț Minim",
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    
    pret_max = forms.DecimalField(
        required=False, 
        min_value=0, 
        label="Preț Maxim",
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

    categorie = forms.ModelChoiceField(
        queryset=Categorie.objects.all(),
        required=False,
        label="Categorie",
        empty_label="Toate Categoriile",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    doar_noi = forms.BooleanField(
        required=False, 
        label="Doar modele noi (>2023)",
        widget=forms.CheckboxInput()
    )

    def clean(self):
        cleaned_data = super().clean()
        pret_min = cleaned_data.get('pret_min')
        pret_max = cleaned_data.get('pret_max')

        if pret_min and pret_max and pret_min > pret_max:
            raise forms.ValidationError("Prețul minim nu poate fi mai mare decât prețul maxim!")

        nume = cleaned_data.get('nume')
        if nume and len(nume) < 2:
            self.add_error('nume', "Te rog introdu minim 2 caractere pentru căutare.")

        return cleaned_data
    

def validate_major(data_nasterii):
    today = date.today()
    varsta = today.year - data_nasterii.year - ((today.month, today.day) < (data_nasterii.month, data_nasterii.day))
    if varsta < 18:
        raise ValidationError("Trebuie să aveți peste 18 ani.")

def validate_cnp(value):
    if not value.isdigit():
        raise ValidationError("CNP-ul trebuie să conțină doar cifre.")

    if len(value) != 13:
        raise ValidationError("CNP-ul trebuie să aibă exact 13 caractere.")

    if value[0] not in ['1', '2', '5', '6']:
        raise ValidationError("CNP invalid (prima cifră incorectă).")

    an = int(value[1:3])
    luna = int(value[3:5])
    zi = int(value[5:7])

    if value[0] in ['1', '2']: an += 1900
    elif value[0] in ['5', '6']: an += 2000
    
    try:
        date(an, luna, zi)
    except ValueError:
        raise ValidationError("CNP-ul nu conține o dată validă.")

def validate_nume_format(value):
    if not value: return
    
    if not re.match(r'^[A-Z][a-zA-Z\s\-]*$', value):
        raise ValidationError("Trebuie să înceapă cu literă mare și să conțină doar litere, spații sau cratimă.")

    separators = re.split(r'[\s\-]', value)
    for part in separators:
        if part and not part[0].isupper():
            raise ValidationError("Fiecare nume trebuie să înceapă cu literă mare (după spațiu sau cratimă).")

def validate_email_custom(value):
    domenii_interzise = ['guerillamail.com', 'yopmail.com']
    domain = value.split('@')[-1]
    if domain in domenii_interzise:
        raise ValidationError(f"Domeniul {domain} nu este acceptat.")

def validate_fara_linkuri(value):
    if 'http://' in value or 'https://' in value:
        raise ValidationError("Nu sunt permise link-uri în text.")

def validate_mesaj_text(value):
    validate_fara_linkuri(value)

    words = re.findall(r'\w+', value)
    if not (5 <= len(words) <= 100):
        raise ValidationError(f"Mesajul trebuie să aibă între 5 și 100 cuvinte (are {len(words)}).")

    for w in words:
        if len(w) > 15:
            raise ValidationError(f"Cuvântul '{w}' este prea lung (max 15 caractere).")


class ContactForm(forms.Form):
    TIPURI_MESAJ = (
        ('neselectat', 'Selectează tip...'),
        ('reclamatie', 'Reclamație'),
        ('intrebare', 'Întrebare'),
        ('review', 'Review'),
        ('cerere', 'Cerere'),
        ('programare', 'Programare'),
    )

    nume = forms.CharField(max_length=10, validators=[validate_nume_format], widget=forms.TextInput(attrs={'class': 'form-control'}))
    prenume = forms.CharField(max_length=10, required=False, validators=[validate_nume_format], widget=forms.TextInput(attrs={'class': 'form-control'}))
    cnp = forms.CharField(min_length=13, max_length=13, required=False, validators=[validate_cnp], widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Optional'}))
    
    data_nasterii = forms.DateField(
        validators=[validate_major],
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    
    email = forms.EmailField(validators=[validate_email_custom], widget=forms.EmailInput(attrs={'class': 'form-control'}))
    confirmare_email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    
    tip_mesaj = forms.ChoiceField(choices=TIPURI_MESAJ, initial='neselectat', widget=forms.Select(attrs={'class': 'form-control'}))
    
    subiect = forms.CharField(max_length=100, validators=[validate_nume_format, validate_fara_linkuri], widget=forms.TextInput(attrs={'class': 'form-control'}))
    
    zile_asteptare = forms.IntegerField(
        min_value=1, max_value=30,
        label="Câte zile puteți aștepta?",
        help_text="Review/Cereri: minim 4 zile. Cereri/Intrebari: minim 2 zile. Max 30.",
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    
    mesaj = forms.CharField(
        label="Mesaj (Semnează-te cu numele tău la final!)",
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        validators=[validate_mesaj_text]
    )

    def clean(self):
        cleaned_data = super().clean()
        
        email = cleaned_data.get('email')
        conf_email = cleaned_data.get('confirmare_email')
        mesaj = cleaned_data.get('mesaj')
        nume = cleaned_data.get('nume')
        tip = cleaned_data.get('tip_mesaj')
        zile = cleaned_data.get('zile_asteptare')
        cnp = cleaned_data.get('cnp')
        data_nasterii = cleaned_data.get('data_nasterii')

        if email and conf_email and email != conf_email:
            self.add_error('confirmare_email', "Adresele de email nu coincid.")

        if tip == 'neselectat':
            self.add_error('tip_mesaj', "Vă rugăm selectați un tip de mesaj.")

        if mesaj and nume:
            words = re.findall(r'\w+', mesaj)
            if not words or words[-1].lower() != nume.lower():
                self.add_error('mesaj', f"Mesajul trebuie să se termine cu numele dumneavoastră ({nume}).")

        if zile and tip:
            if tip in ['review', 'cerere'] and zile < 4:
                self.add_error('zile_asteptare', f"Pentru {tip} trebuie să așteptați minim 4 zile.")
            elif tip in ['intrebare', 'cerere'] and zile < 2: 
                self.add_error('zile_asteptare', f"Pentru {tip} trebuie să așteptați minim 2 zile.")

        if cnp and data_nasterii:
            an_cnp = int(cnp[1:3])
            if cnp[0] in ['1', '2']: an_cnp += 1900
            elif cnp[0] in ['5', '6']: an_cnp += 2000
            
            luna_cnp = int(cnp[3:5])
            zi_cnp = int(cnp[5:7])
            
            if not (an_cnp == data_nasterii.year and luna_cnp == data_nasterii.month and zi_cnp == data_nasterii.day):
                self.add_error('cnp', "CNP-ul nu corespunde cu data nașterii introdusă.")
                
        return cleaned_data

def validate_pozitiv(value):
    if value < 0:
        raise ValidationError("Valoarea trebuie să fie pozitivă.")

def validate_nu_exagerat(value):
    if value > 100000:
        raise ValidationError("Valoarea este suspect de mare.")

class MotocicletaForm(forms.ModelForm):
    pret_achizitie = forms.DecimalField(
        label="Preț de achiziție (EUR)",
        validators=[validate_pozitiv],
        help_text="Prețul cu care a fost cumpărată motocicleta."
    )
    
    adaos_procent = forms.IntegerField(
        label="Adaos Comercial (%)",
        min_value=0, max_value=500,
        help_text="Procentul adăugat la preț (ex: 20 pentru 20%).",
        validators=[validate_pozitiv]
    )

    class Meta:
        model = Motocicleta
        exclude = ['pret', 'data_introducere', 'piese'] 

        labels = {
            'serie_sasiu': 'VIN (Serie Șasiu)',
            'an_fabricatie': 'Anul de fabricație'
        }

        help_texts = {
            'serie_sasiu': 'Trebuie să fie unic.',
        }

        widgets = {
            'an_fabricatie': forms.NumberInput(attrs={'min': 1900, 'max': 2026, 'class': 'form-control'}),
            'descriere': forms.Textarea(attrs={'rows': 3}),
        }

    def clean_an_fabricatie(self):
        an = self.cleaned_data['an_fabricatie']
        if an > datetime.now().year:
            raise ValidationError("Anul fabricației nu poate fi în viitor!")
        return an

    def clean_serie_sasiu(self):
        serie = self.cleaned_data['serie_sasiu']
        if len(serie) < 5:
            raise ValidationError("Seria de șasiu e prea scurtă.")
        if not serie.isalnum():
             raise ValidationError("Seria trebuie să conțină doar litere și cifre.")
        return serie

    def clean(self):
        cleaned_data = super().clean()
        motor = cleaned_data.get('motor')
        categorie = cleaned_data.get('categorie')

        if motor and categorie:
            if 'Sport' in categorie.nume and motor.putere_cp < 50:
                 raise forms.ValidationError("O motocicletă Sport trebuie să aibă un motor de minim 50 CP!")
                 
        return cleaned_data
    

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'telefon', 'adresa', 'oras', 'judet', 'newsletter')
        
    def clean_oras(self):
        oras = self.cleaned_data.get('oras')
        if oras and not oras[0].isupper():
            raise forms.ValidationError("Orașul trebuie să înceapă cu literă mare.")
        return oras
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        email_utilizator = self.cleaned_data.get('email', 'N/A')

        if username.lower() == 'admin':
            subiect = "cineva incearca sa ne preia site-ul"
            mesaj_text = f"Tentativa de inregistrare cu user 'admin' de pe adresa: {email_utilizator}"

            mesaj_html = f"""
                <h1 style='color: red;'>{subiect}</h1>
                <p>Tentativa de inregistrare cu user 'admin'.</p>
                <p>Email suspect: {email_utilizator}</p>
            """
            
            mail_admins(subiect, mesaj_text, html_message=mesaj_html)
            
            raise forms.ValidationError("Acest username este rezervat.")
        
        return username

class CustomLoginForm(AuthenticationForm):
    remember_me = forms.BooleanField(
        required=False, 
        label="Ține-mă minte (1 zi)", 
        widget=forms.CheckboxInput()
    )
    
class PromotieForm(forms.ModelForm):
    categorii_tinta = forms.ModelMultipleChoiceField(
        queryset=Categorie.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label="Alege categoriile vizate",
        required=True
    )

class Meta:
        model = Promotie
        fields = ['nume', 'subiect', 'mesaj', 'data_expirare', 'discount', 'cod_promo']
        widgets = {
            'data_expirare': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'mesaj': forms.Textarea(attrs={'rows': 3}),
        }