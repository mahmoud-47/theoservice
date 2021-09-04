from django.shortcuts import render,HttpResponse,get_object_or_404,redirect

def home(request):
	return redirect('accueil')
