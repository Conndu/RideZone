from django.db import models
from django.http import HttpResponse
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
import uuid

class CustomUser(AbstractUser):
    telefon = models.CharField(max_length=15, blank=True, help_text="Număr de telefon.")
    adresa = models.CharField(max_length=100, blank=True, help_text="Adresa completă.")
    oras = models.CharField(max_length=50, blank=True)
    judet = models.CharField(max_length=50, blank=True)
    newsletter = models.BooleanField(default=False, help_text="Abonează-te la noutăți.")
    cod = models.CharField(max_length=100, null=True, blank=True)
    email_confirmat = models.BooleanField(default=False)
    
    
    def clean_telefon(self):
        if self.telefon and not self.telefon.isdigit():
             raise ValidationError("Telefonul trebuie să conțină doar cifre.")

    def clean_adresa(self):
        if self.adresa and len(self.adresa) < 5:
             raise ValidationError("Adresa este prea scurtă.")
             
    def __str__(self):
        return self.username
    
    
class Categorie(models.Model):
    nume = models.CharField(max_length=100, unique=True)
    culoare_identificare = models.CharField(max_length = 20, default="#000000", help_text="Cod HEX culoare (ex: #FF0000)")
    descriere = models.CharField(max_length=300, blank=True)

    class Meta:
        verbose_name_plural = "Categorii"

    def __str__(self):
        return self.nume

class Furnizor(models.Model):
    id_furnizor = models.AutoField(primary_key=True)
    nume = models.CharField(max_length=155)
    tara_origine = models.CharField(max_length=100)
    email = models.EmailField()
    
    class Meta:
        verbose_name_plural = "Furnizori"
    
    def __str__(self):
        return self.nume
    
class Piesa(models.Model):
    id_piesa = models.AutoField(primary_key=True)
    nume = models.CharField(max_length=150)    
    pret = models.DecimalField(max_digits=10, decimal_places=2)
    furnizor = models.ForeignKey(Furnizor, on_delete=models.CASCADE)
    garantie_luni = models.IntegerField()
    
    class Meta:
        verbose_name_plural = "Piese"
    
    def __str__(self):
        return self.nume
    

class Motor(models.Model):
    id_motor = models.AutoField(primary_key=True)
    tip = models.CharField(max_length=100)
    capacitate_cc = models.IntegerField()
    consum = models.FloatField()
    putere_cp = models.IntegerField()
    
    class Meta:
        verbose_name_plural = "Motoare"
    
    def __str__(self):
        return f"{self.tip} - {self.capacitate_cc}cc - {self.putere_cp}cp"

class Marca(models.Model):
    id_marca = models.AutoField(primary_key=True)
    nume = models.CharField(max_length=100, unique=True)
    data_creare = models.DateField()
    tara_origine = models.CharField(max_length=100)
    fondator = models.CharField(max_length=100)
    descriere = models.TextField(blank=True)
    
    class Meta:
        verbose_name_plural = "Marci"

    def __str__(self):
        return self.nume
    
    
class Motocicleta(models.Model):
    id_motocicleta = models.AutoField(primary_key=True)
    serie_sasiu = models.CharField(max_length=100, unique=True)
    model = models.CharField(max_length=100)
    an_fabricatie = models.IntegerField()
    pret = models.DecimalField(max_digits=10, decimal_places=2)
    data_introducere = models.DateField()
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE)
    marca = models.ForeignKey(Marca, on_delete=models.CASCADE)
    motor = models.ForeignKey(Motor, on_delete=models.CASCADE)
    piese = models.ManyToManyField(Piesa, blank=True)
    
    class Meta:
        verbose_name_plural = "Motociclete"
    
    def __str__ (self):
        return f"{self.marca.nume} {self.model} ({self.serie_sasiu})"
    
class Vizualizare(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    produs = models.ForeignKey(Motocicleta, on_delete=models.CASCADE)
    data_vizualizare = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.produs.model}"

class Promotie(models.Model):
    nume = models.CharField(max_length=100)
    data_creare = models.DateTimeField(auto_now_add=True)
    data_expirare = models.DateField()
    subiect = models.CharField(max_length=100)
    mesaj = models.TextField()

    discount = models.IntegerField(help_text="Procent reducere (ex: 15)")
    cod_promo = models.CharField(max_length=20, help_text="Ex: MOTO2024")

    categorii = models.ManyToManyField(Categorie, blank=True)

    def __str__(self):
        return self.nume
    