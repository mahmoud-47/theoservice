from django.contrib import admin
from .models import Contact,Cathegorie,Commande,Produit,Message,User

admin.site.register(Cathegorie)
admin.site.register(Message)

class CommandeInline(admin.TabularInline):
	model = Commande
	fieldsets=[
		('None',{'fields':['produit','contacted']})
	]
	extra = 0




@admin.register(Produit)
class AdminProduit(admin.ModelAdmin):
	search_fields=['nom']

@admin.register(Commande)
class AdminCommande(admin.ModelAdmin):
	search_fields=['produit','user']
	list_filter=['date','contacted','commanded','paied']
	
