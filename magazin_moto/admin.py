from django.contrib import admin
from .models import Motocicleta, Categorie, Marca, Motor, Furnizor, Piesa


admin.site.site_header = "Administrare Magazin Moto"
admin.site.site_title = "Admin Moto"
admin.site.index_title = "Panou de Control"

class CategorieAdmin(admin.ModelAdmin):
    list_display = ('nume', 'culoare_identificare' ,'descriere')
    
class MotocicletaAdmin(admin.ModelAdmin):
    list_display = ( 'marca', 'model', 'an_fabricatie', 'pret', 'categorie', 'motor')
    ordering = ['-pret']
    search_fields = ['model' , 'marca__nume']
    list_filter = ('categorie', 'an_fabricatie', 'marca')
    list_per_page = 5
    fieldsets = (
        ('Informatii generale', {
            'fields': ('marca', 'model', 'pret', 'categorie')
        }),
        ('Detalii tehnice', {
            'classes': ('collapse',),
            'fields': ('motor', 'an_fabricatie', 'serie_sasiu', 'data_introducere', 'piese')
        }),
    )
    empty_value_display = '-gol-'
    
class MotorAdmin(admin.ModelAdmin):
    list_display = ('tip', 'capacitate_cc', 'putere_cp')
    
class MarcaAdmin(admin.ModelAdmin):
    list_display = ('nume', 'data_creare', 'tara_origine', 'fondator')
    search_fields = ('nume', 'tara_origine')

class FurnizorAdmin(admin.ModelAdmin):
    list_display = ('nume', 'tara_origine', 'email')
    
class PiesaAdmin(admin.ModelAdmin):
    list_display = ('nume', 'pret', 'furnizor', 'garantie_luni')
    

admin.site.register(Piesa, PiesaAdmin)
admin.site.register(Furnizor, FurnizorAdmin)    
admin.site.register(Marca, MarcaAdmin)
admin.site.register(Motor, MotorAdmin)
admin.site.register(Motocicleta, MotocicletaAdmin)
admin.site.register(Categorie, CategorieAdmin)
