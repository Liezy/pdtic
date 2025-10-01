from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.template.loader import render_to_string
from .models import PDTIC, VersaoPDTIC
from .forms import PDTICForm, VersaoPDTICForm
from instituicoes.models import Instituicao

def pdtic_list(request):
    # Filtra PDTICs pela instituição ativa
    if hasattr(request, 'instituicao_ativa'):
        planos = PDTIC.objects.filter(instituicao=request.instituicao_ativa)
    else:
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
    # Filtra PDTIC pela instituição ativa
    if hasattr(request, 'instituicao_ativa'):
        plano = get_object_or_404(PDTIC, pk=pk, instituicao=request.instituicao_ativa)
    else:
        plano = get_object_or_404(PDTIC, pk=pk)
    return render(request, "pdtic/pdtic_detail.html", {"plano": plano})

def pdtic_create(request):
    instituicao_ativa = getattr(request, 'instituicao_ativa', None)
    
    if request.method == "POST":
        form = PDTICForm(request.POST, instituicao_ativa=instituicao_ativa)
        if form.is_valid():
            # Define a instituição ativa automaticamente
            if instituicao_ativa:
                pdtic = form.save(commit=False)
                pdtic.instituicao = instituicao_ativa
                pdtic.save()
            else:
                form.save()
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': True})
            else:
                return redirect("pdtic_list")
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                html = render_to_string('pdtic/pdtic_form_modal.html', {'form': form}, request=request)
                return JsonResponse({'success': False, 'form_html': html})
            else:
                return render(request, "pdtic/pdtic_form.html", {"form": form})
    else:
        # Cria form com instituição ativa se disponível
        form = PDTICForm(instituicao_ativa=instituicao_ativa)
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render(request, "pdtic/pdtic_form_modal.html", {"form": form})
    return render(request, "pdtic/pdtic_form.html", {"form": form})


def pdtic_update(request, pk):
    instituicao_ativa = getattr(request, 'instituicao_ativa', None)
    
    # Garante que só pode editar PDTICs da instituição ativa
    if instituicao_ativa:
        plano = get_object_or_404(PDTIC, pk=pk, instituicao=instituicao_ativa)
    else:
        plano = get_object_or_404(PDTIC, pk=pk)
        
    if request.method == "POST":
        form = PDTICForm(request.POST, instance=plano, instituicao_ativa=instituicao_ativa)
        if form.is_valid():
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                form.save()
                return JsonResponse({'success': True})
            else:
                form.save()
                return redirect("pdtic_detail", pk=plano.pk)
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                html = render_to_string('pdtic/pdtic_form_modal.html', {'form': form, 'object': plano}, request=request)
                return JsonResponse({'success': False, 'form_html': html})
            else:
                return render(request, "pdtic/pdtic_form.html", {"form": form, "object": plano})
    else:
        form = PDTICForm(instance=plano, instituicao_ativa=instituicao_ativa)
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render(request, "pdtic/pdtic_form_modal.html", {"form": form, "object": plano})
    return render(request, "pdtic/pdtic_form.html", {"form": form, "object": plano})


# Views para gerenciar versões do PDTIC
def versao_list(request, pdtic_pk):
    pdtic = get_object_or_404(PDTIC, pk=pdtic_pk)
    versoes = pdtic.versoes.all().order_by('-criado_em')
    return render(request, "pdtic/versao_list.html", {"pdtic": pdtic, "versoes": versoes})


def versao_create(request, pdtic_pk):
    pdtic = get_object_or_404(PDTIC, pk=pdtic_pk)
    if request.method == "POST":
        form = VersaoPDTICForm(request.POST, request.FILES)
        if form.is_valid():
            versao = form.save(commit=False)
            versao.pdtic = pdtic
            versao.save()
            return redirect("versao_list", pdtic_pk=pdtic.pk)
    else:
        form = VersaoPDTICForm()
    return render(request, "pdtic/versao_form.html", {"form": form, "pdtic": pdtic})


def versao_detail(request, pdtic_pk, pk):
    pdtic = get_object_or_404(PDTIC, pk=pdtic_pk)
    versao = get_object_or_404(VersaoPDTIC, pk=pk, pdtic=pdtic)
    return render(request, "pdtic/versao_detail.html", {"pdtic": pdtic, "versao": versao})


def versao_update(request, pdtic_pk, pk):
    pdtic = get_object_or_404(PDTIC, pk=pdtic_pk)
    versao = get_object_or_404(VersaoPDTIC, pk=pk, pdtic=pdtic)
    if request.method == "POST":
        form = VersaoPDTICForm(request.POST, request.FILES, instance=versao)
        if form.is_valid():
            form.save()
            return redirect("versao_detail", pdtic_pk=pdtic.pk, pk=versao.pk)
    else:
        form = VersaoPDTICForm(instance=versao)
    return render(request, "pdtic/versao_form.html", {"form": form, "pdtic": pdtic, "object": versao})


def versao_delete(request, pdtic_pk, pk):
    pdtic = get_object_or_404(PDTIC, pk=pdtic_pk)
    versao = get_object_or_404(VersaoPDTIC, pk=pk, pdtic=pdtic)
    if request.method == "POST":
        versao.delete()
        return redirect("versao_list", pdtic_pk=pdtic.pk)
    return render(request, "pdtic/versao_confirm_delete.html", {"pdtic": pdtic, "versao": versao})