from django.shortcuts import render


def destination_list(request):
    return render(request, "pages/destinations.html")
