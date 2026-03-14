from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
	path("", views.index, name="index"),
	path("info/", views.info, name="info"),
	path("exemplu/", views.afis_template, name="exemplu"),
	path("log/", views.log_view, name = "log"),
	path("produse/", views.produse_view, name="produse"),
	path("produse/<int:id_motocicleta>/", views.produs_detail, name="produs_detail"),
	path("categorii/<str:nume_categorie>/", views.categorie_view, name="categorie_view"),
 	path("contact/", views.contact_view, name="contact"),
	path("adauga/", views.adauga_motocicleta_view, name="adauga_moto"),
 	path("inregistrare/", views.inregistrare_view, name="inregistrare"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("profil/", views.profil_view, name="profil"),
    path("schimba-parola/", auth_views.PasswordChangeView.as_view(template_name="magazin_moto/change_password.html", success_url='/profil/'), name="password_change"),
    path('confirma_mail/<str:cod>/', views.confirma_mail_view, name='confirma_mail'),
    path('promotii/', views.promotii_view, name='promotii'),    
]
