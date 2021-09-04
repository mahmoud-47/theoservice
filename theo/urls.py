from django.urls import path
from . import views

urlpatterns = [
    path('',views.accueil,name='accueil'),
    path('compte/',views.compte,name='compte'),
    path('login/',views.login_view,name='login_view'),
    path('register/',views.register_view,name='register_view'),
    path('logout/',views.logout_view,name='logout'),
    path('contact/',views.contact,name='contact'),
    path('detail/<int:id>',views.detail_produit,name='detail_produit'),
    path('ajout_panier/<int:id_produit>',views.ajout_panier,name='ajout_panier'),
    path('supp_panier/<int:id_produit>',views.supp_panier,name='supp_panier'),
    path('supp_commande/<int:id_produit>',views.supp_commande,name='supp_commande'),
    path('nom_panier/',views.mon_panier,name='mon_panier'),
    path('vider_panier/',views.vider_panier,name='vider_panier'),
    path('confirm/',views.confirm,name='confirm'),
]

