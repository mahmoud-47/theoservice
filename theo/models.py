from django.db import models
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import User
from django.core.validators import MaxLengthValidator


class Contact(models.Model):
	user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
	adresse = models.CharField(max_length=200)
	phone = models.CharField(max_length=20)
	date = models.DateTimeField(auto_now_add=True)
	def __str__(self):
		return self.user.first_name+' '+self.user.last_name

class Cathegorie(models.Model):
	nom=models.CharField(max_length=30)
	date = models.DateTimeField(auto_now_add=True)
	def __str__(self):
		return self.nom

class Produit(models.Model):
	image= CloudinaryField('image',null=True)
	nom = models.CharField(max_length=20)
	cath = models.ForeignKey(Cathegorie,on_delete=models.CASCADE)
	dispo = models.BooleanField('disponible',default=True)
	detail = models.CharField(max_length=1000,default='')
	date = models.DateTimeField(auto_now_add=True)
	prix = models.CharField(max_length=10,null=True)
	def __str__(self):
		return self.nom


class Commande(models.Model):
	produit = models.ForeignKey(Produit,on_delete=models.CASCADE)
	user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
	contacted = models.BooleanField('Contacté',default=False)
	date = models.DateTimeField(auto_now_add=True)
	qte = models.IntegerField(default=1)
	paied = models.BooleanField("Payé",default=False)
	commanded = models.BooleanField(default=False)
	def __str__(self):
		signe = '-'
		if self.contacted:
			signe = '+'
		prod = self.produit.nom
		user = self.user.first_name+' '+self.user.last_name
		return '({}) {} - {}'.format(signe,prod,user)

class Message(models.Model):
	prenom = models.CharField(max_length=30)
	nom = models.CharField(max_length=20)
	email = models.EmailField()
	phone = models.CharField(max_length=20)
	message=models.TextField(max_length=150,blank=True,validators=[MaxLengthValidator(150)])
	date = models.DateTimeField(auto_now_add=True)
	def __str__(self):
		return self.prenom
