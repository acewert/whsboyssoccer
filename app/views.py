from django.shortcuts import render


def home(request):
	return render(request, 'home.html')


def roster(request):
	return render(request, 'roster.html')


def schedule(request):
	return render(request, 'schedule.html')


def coaches(request):
	return render(request, 'coaches.html')


def history(request):
	return render(request, 'history.html')


def photos(request):
	return render(request, 'photos.html')


def sponsor(request):
	return render(request, 'sponsor.html')