from django.shortcuts import render, get_object_or_404, redirect
from .models import PDTIC
from .forms import PDTICForm
from instituicoes.models import Instituicao

def pdtic_list(request):
    planos = PDTIC.objects.all()
    return render(request, "pdtic/pdtic_list.html", {"planos": planos})

def pdtic_list_by_instituicao(request, instituicao_pk):
    instituicao = get_object_or_404(Instituicao, pk=instituicao_pk)
    planos = PDTIC.objects.filter(instituicao=instituicao)
    return render(request, "pdtic/pdtic_list.html", {
        "planos": planos, 
        "instituicao": instituicao
    })

def pdtic_detail(request, pk):
    plano = get_object_or_404(PDTIC, pk=pk)
    return render(request, "pdtic/pdtic_detail.html", {"plano": plano})

def pdtic_create(request):
    if request.method == "POST":
        form = PDTICForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("pdtic_list")
    else:
        form = PDTICForm()
    return render(request, "pdtic/pdtic_form.html", {"form": form})