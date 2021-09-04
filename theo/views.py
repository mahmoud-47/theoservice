from django.shortcuts import render,HttpResponse,redirect,get_object_or_404
from .models import Contact,Cathegorie,Commande,Produit,User,Message
from django.contrib.auth import login,logout,authenticate
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage

cathegories = Cathegorie.objects.all()

def accueil(request):
	produits=Produit.objects.all().filter(dispo=True).order_by('-date')
	nb_panier = Commande.objects.all().filter(commanded=False,user=request.user).count()
	search = request.GET.get('search')
	if request.method=='POST':
		cath = request.POST.get('cath')
		produits=Produit.objects.all().filter(dispo=True,cath__nom=cath).order_by('-date')
		msg= f'Produits triés par "{cath}"'
		context={'cathegories':cathegories,'produits':produits,'nb_panier':nb_panier,"msg":msg}
	elif search:
		produits =Produit.objects.all().filter(dispo=True,detail__icontains=search).order_by('-date')|Produit.objects.all().filter(dispo=True,nom__icontains=search).order_by('-date')
		msg = f'La recherche avec "{search}" a donné {produits.count()} résultats'
		context={'cathegories':cathegories,'produits':produits,'nb_panier':nb_panier,'msg':msg}
	else:
		prod_list=Produit.objects.all().filter(dispo=True).order_by('-date')
		paginator = Paginator(prod_list,24)
		page=request.GET.get('page')
		if not page :
			page = 1
		try:
			produits=paginator.page(page)
		except PageNotAnInteger:
			produits=paginator.page(1)
		except EmptyPage:
			produits=paginator.page(paginator.num_pages)
		context={'cathegories':cathegories,'produits':produits,'nb_panier':nb_panier,'page':page}
	return render(request,'home.html',context)
	

def compte(request):
	prods = Commande.objects.all().filter(user=request.user,commanded=True,paied=False)
	histos = Commande.objects.all().filter(user=request.user,paied=True)

	produits=[]
	historiques = []

	for panier in prods:
		prod={}
		prod['id']=panier.produit.id
		prod['image']= panier.produit.image
		prod['nom'] = panier.produit.nom
		prod['prix'] = panier.produit.prix
		prod['nb'] = panier.qte
		produits.append(prod)

	for panier in histos:
		prod={}
		prod['id']=panier.produit.id
		prod['image']= panier.produit.image
		prod['nom'] = panier.produit.nom
		prod['prix'] = panier.produit.prix
		prod['nb'] = panier.qte
		prod['date'] = panier.date
		historiques.append(prod)

	nb_panier = Commande.objects.all().filter(commanded=False,user=request.user).count()
	er=""
	cathegories = Cathegorie.objects.all()
	if request.user.is_authenticated:
		if request.method=='POST':
			user=User.objects.get(id=request.user.id)
			user.first_name=request.POST.get('prenom').strip()
			user.last_name=request.POST.get('nom').strip()
			user.email=request.POST.get('email').strip()
			my_users=User.objects.filter(email=user.email)
			if not user.email == request.user.email:
				if not my_users.exists():
					user.username=request.POST.get('email').strip()
					user.save()
					contact=Contact.objects.get(user=user)
					contact.adresse=request.POST.get('adresse').strip()
					contact.phone=request.POST.get('phone').strip()
					contact.save()
					contact = Contact.objects.get(user=user)
					return render(request,'compte.html',{'er':'Modifié avec succés','user':user,'contact':contact,'cathegories':cathegories,'nb_panier':nb_panier})
				else:
					contact = Contact.objects.get(user=request.user)
					return render(request,'compte.html',{'er':'Adresse mail déja pris','user':user,'contact':contact,'cathegories':cathegories,'nb_panier':nb_panier,'produits':produits,'historiques':historiques})
			else:
				user.save()
				contact = Contact.objects.get(user=user)
				return render(request,'compte.html',{'er':'Modifié avec succés','user':user,'contact':contact,'cathegories':cathegories,'nb_panier':nb_panier,'produits':produits,'historiques':historiques})
		else:
			try:
				contact = Contact.objects.get(user=request.user)
			except:
				contact={
					'adresse':'',
					'phone':''
				}
			context={'user':request.user,'contact':contact,'cathegories':cathegories,'nb_panier':nb_panier,'produits':produits,'historiques':historiques}
			return render(request,'compte.html',context)
	else:
		return redirect('home')

def login_view(request):
	er=''
	cathegories = Cathegorie.objects.all()
	if request.user.is_authenticated:
		return redirect('home')
	if request.method=='POST':
		email = request.POST.get('email').strip()
		mdp = request.POST.get('password').strip()
		user=authenticate(username=email,password=mdp)
		if user is not None:
			login(request,user)
			return redirect('home')
		else:
			er+="Erreur d'authentification"
			return render(request,'login.html',{'er':er,'cathegories':cathegories})
	else:
		return render(request,'login.html',{'cathegories':cathegories})

def register_view(request):
    er=''
    cathegories = Cathegorie.objects.all()
    if request.user.is_authenticated:
        return redirect('home')
    if request.method=="POST":
    	prenom = request.POST.get('prenom').strip()
    	nom=request.POST.get('nom').strip()
    	password=request.POST.get('password').strip()
    	password2 = request.POST.get('password2').strip()
    	email = request.POST.get("email").strip()
    	adresse = request.POST.get('adresse').strip()
    	phone = request.POST.get('phone').strip()
    	if password==password2:
    		one=User.objects.filter(email=email)
    		if not one:
    			try:
    				user=User.objects.create_user(
    					first_name = prenom,
    					last_name = nom,
    					email = email,
    					password = password,
    					username=email,
    				)
    				contact = Contact()
    				contact.user = user
    				contact.adresse = adresse
    				contact.phone = phone
    				contact.save()
    				return redirect('login_view')
    			except:
    				er+="Une erreur s'est produite. Réessayez avec une autre adresse mail !"
    				return render(request, 'register.html', {'er': er,'cathegories':cathegories})
    		else:
    			er='Adresse Mail déja prise'
    			return render(request, 'register.html', {'er': er,'cathegories':cathegories})
    	else:
    		er='Les mot de passe ne sont pas identiques'
    		return render(request, 'register.html', {'er': er,'cathegories':cathegories})
    else:
        return render(request, 'register.html', {'er': er,'cathegories':cathegories}) 

def logout_view(request):
	if not request.user.is_authenticated:
		return redirect('home')
	logout(request)
	return redirect('login_view')

def contact(request):
	nb_panier = Commande.objects.all().filter(commanded=False,user=request.user).count()
	er=''
	if request.method=='POST':
		mess=Message()
		mess.prenom = request.POST.get('prenom').strip()
		mess.nom = request.POST.get('nom').strip()
		mess.email = request.POST.get('email').strip()
		mess.phone = request.POST.get('phone').strip()
		mess.message = request.POST.get('message').strip()
		mess.save()
		try:
			contact=Contact.objects.get(user=request.user)
		except:
			contact=Contact()
		er="Méssage envoyé avec succés"
		context={'er':er,'contact':contact,'nb_panier':nb_panier}
		return render(request,'contact.html',context)
	else:
		try:
			contact=Contact.objects.get(user=request.user)
		except:
			contact=Contact()
		context={'er':er,'contact':contact,'nb_panier':nb_panier}
		return render(request,'contact.html',context)

def detail_produit(request,id):
	nb_panier = Commande.objects.all().filter(commanded=False,user=request.user).count()
	produit = get_object_or_404(Produit,pk=id)
	context={'nb_panier':nb_panier,'cathegories':cathegories,'produit':produit}
	return render(request,'detail_produit.html',context)

def ajout_panier(request,id_produit):
	nb_panier = Commande.objects.all().filter(commanded=False,user=request.user).count()
	er=''
	if not request.user.is_authenticated:
		er="Vous devez d'abord vous connnecter pour réserver"
		context={'er':er,'nb_panier':nb_panier}
		return render(request,'login.html',context)
	prod = get_object_or_404(Produit,pk=id_produit)
	user = request.user
	my_comms = Commande.objects.all().filter(user=user,produit=prod)
	if not my_comms.exists():
		panier = Commande.objects.create(
			user = user,
			produit = prod,
		)
	return redirect('detail_produit',id = id_produit)

def mon_panier(request):
	if not request.user.is_authenticated:
		return redirect('home')
	if request.method=='POST':
		prod = get_object_or_404(Produit,pk=request.POST.get('id'))
		pan = Commande.objects.get(produit=prod,user=request.user,commanded=False)
		pan.qte = request.POST.get('nb')
		pan.save()
	nb_panier = Commande.objects.all().filter(commanded=False,user=request.user).count()
	paniers = Commande.objects.all().filter(user=request.user,commanded=False)
	vide = True
	if paniers.exists():
		vide = False
	produits=[]
	for panier in paniers:
		prod={}
		prod['id']=panier.produit.id
		prod['image']= panier.produit.image
		prod['nom'] = panier.produit.nom
		prod['prix'] = panier.produit.prix
		prod['nb'] = panier.qte
		produits.append(prod)
	context={'produits':produits,'nb_panier':nb_panier,'cathegories':cathegories,'vide':vide}
	return render(request,'panier.html',context)

def supp_panier(request,id_produit):
	if not request.user.is_authenticated:
		return redirect('home')
	if not request.user.is_authenticated:
		return redirect('home')
	prod = get_object_or_404(Produit,pk=id_produit)
	try:
		pan = Commande.objects.get(produit=prod,user=request.user,commanded=False)
		pan.delete()
		return redirect('mon_panier')
	except:
		return redirect('mon_panier')

def vider_panier(request):
	if not request.user.is_authenticated:
		return redirect('home')
	pans = Commande.objects.all().filter(user=request.user,commanded=False)
	for pan in pans:
		pan.delete()
	return redirect('mon_panier')

def confirm(request):
	nb_panier = Commande.objects.all().filter(commanded=False,user=request.user).count()
	er=""
	cathegories = Cathegorie.objects.all()
	if request.user.is_authenticated:
		if request.method=='POST':
			user=User.objects.get(id=request.user.id)
			user.first_name=request.POST.get('prenom').strip()
			user.last_name=request.POST.get('nom').strip()
			user.email=request.POST.get('email').strip()
			my_users=User.objects.filter(email=user.email)
			if not user.email == request.user.email:
				if not my_users.exists():
					user.username=request.POST.get('email').strip()
					user.save()
					contact=Contact.objects.get(user=user)
					contact.adresse=request.POST.get('adresse').strip()
					contact.phone=request.POST.get('phone').strip()
					contact.save()
					contact = Contact.objects.get(user=user)
					comms = Commande.objects.filter(commanded=False,user=request.user)
					for comm in comms:
						comm.commanded=True
						comm.save()
					msg= f"Salut {user.first_name}, Votre commande a été éffectuée avec succés et sera disponible d'ici 3 jours (Dimanche exclus). Un de nos agents vous contactera lorsque votre produit sera disponible. Assurez vous d'avoir la monnaie. Merci"
					nb_panier = Commande.objects.all().filter(commanded=False,user=request.user).count()
					return render(request,'prototype.html',{'msg':msg,'user':user,'contact':contact,'cathegories':cathegories,'nb_panier':nb_panier})
				else:
					contact = Contact.objects.get(user=request.user)
					nb_panier = Commande.objects.all().filter(commanded=False,user=request.user).count()
					return render(request,'confirm.html',{'er':'Adresse mail déja pris','user':user,'contact':contact,'cathegories':cathegories,'nb_panier':nb_panier})
			else:
				comms = Commande.objects.filter(commanded=False,user=request.user)
				for comm in comms:
					comm.commanded=True
					comm.save()
				user.save()
				contact = Contact.objects.get(user=user)
				nb_panier = Commande.objects.all().filter(commanded=False,user=request.user).count()
				msg= f"Salut {user.first_name}, Votre commande a été éffectuée avec succés et sera disponible d'ici 3 jours (Dimanche exclus). Un de nos agents vous contactera lorsque votre produit sera disponible. Assurez vous d'avoir la monnaie. Merci"
				return render(request,'prototype.html',{'msg':msg,'user':user,'contact':contact,'cathegories':cathegories,'nb_panier':nb_panier})
				
		else:
			try:
				contact = Contact.objects.get(user=request.user)
			except:
				contact={
					'adresse':'',
					'phone':''
				}
			nb_panier = Commande.objects.all().filter(commanded=False,user=request.user).count()
			context={'user':request.user,'contact':contact,'cathegories':cathegories,'nb_panier':nb_panier}
			return render(request,'confirm.html',context)
	else:
		return redirect('home')

def supp_commande(request,id_produit):
	if not request.user.is_authenticated:
		return redirect('home')
	if not request.user.is_authenticated:
		return redirect('home')
	prod = get_object_or_404(Produit,pk=id_produit)
	try:
		pan = Commande.objects.get(produit=prod,user=request.user,commanded=False,paied=True)
		pan.delete()
		return redirect('mon_compte')
	except:
		return redirect('mon_compte')