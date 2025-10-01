from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.http import JsonResponse
from django.template.loader import render_to_string
from .models import Instituicao, UnidadeAdministrativa

# --- Instituição ---
class InstituicaoList(ListView):
    model = Instituicao

class InstituicaoDetail(DetailView):
    model = Instituicao
    template_name = 'instituicoes/instituicao_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        instituicao = self.get_object()
        context['unidades_count'] = instituicao.unidades.count()
        context['pdtics_count'] = instituicao.planos.count()
        return context

class InstituicaoCreate(CreateView):
    model = Instituicao
    fields = ['nome', 'sigla']
    success_url = reverse_lazy('instituicao_list')
    
    def get_template_names(self):
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return ['instituicoes/instituicao_form_modal.html']
        return ['instituicoes/instituicao_form.html']
    
    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        
        if form.is_valid():
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                form.save()
                return JsonResponse({'success': True})
            else:
                return self.form_valid(form)
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                html = render_to_string('instituicoes/instituicao_form_modal.html', {'form': form}, request=request)
                return JsonResponse({'success': False, 'form_html': html})
            else:
                return self.form_invalid(form)

class InstituicaoUpdate(UpdateView):
    model = Instituicao
    fields = ['nome', 'sigla']
    success_url = reverse_lazy('instituicao_list')
    
    def get_template_names(self):
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return ['instituicoes/instituicao_form_modal.html']
        return ['instituicoes/instituicao_form.html']
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        
        if form.is_valid():
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                form.save()
                return JsonResponse({'success': True})
            else:
                return self.form_valid(form)
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                html = render_to_string('instituicoes/instituicao_form_modal.html', {'form': form, 'object': self.object}, request=request)
                return JsonResponse({'success': False, 'form_html': html})
            else:
                return self.form_invalid(form)

class InstituicaoDelete(DeleteView):
    model = Instituicao
    success_url = reverse_lazy('instituicao_list')
    
    def get_template_names(self):
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return ['instituicoes/instituicao_confirm_delete_modal.html']
        return ['instituicoes/instituicao_confirm_delete.html']
    
    def post(self, request, *args, **kwargs):
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            self.object = self.get_object()
            self.object.delete()
            return JsonResponse({'success': True})
        else:
            return self.delete(request, *args, **kwargs)


# --- Unidade Administrativa ---
class UnidadeList(ListView):
    model = UnidadeAdministrativa
    template_name = 'unidades/unidade_list.html'
    
    def get_queryset(self):
        # Se vier de uma instituição específica, filtra por ela
        if 'instituicao_pk' in self.kwargs:
            return self.model.objects.filter(instituicao_id=self.kwargs['instituicao_pk'])
        return self.model.objects.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Se vier de uma instituição específica, adiciona ela ao contexto
        if 'instituicao_pk' in self.kwargs:
            context['instituicao'] = Instituicao.objects.get(pk=self.kwargs['instituicao_pk'])
        return context

class UnidadeCreate(CreateView):
    model = UnidadeAdministrativa
    fields = ['nome', 'instituicao']
    template_name = 'unidades/unidade_form.html'
    success_url = reverse_lazy('unidade_list')
    
    def get_template_names(self):
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return ['unidades/unidade_form_modal.html']
        return ['unidades/unidade_form.html']
    
    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        
        if form.is_valid():
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                form.save()
                return JsonResponse({'success': True})
            else:
                return self.form_valid(form)
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                html = render_to_string('unidades/unidade_form_modal.html', {'form': form}, request=request)
                return JsonResponse({'success': False, 'form_html': html})
            else:
                return self.form_invalid(form)

class UnidadeUpdate(UpdateView):
    model = UnidadeAdministrativa
    fields = ['nome', 'instituicao']
    template_name = 'unidades/unidade_form.html'
    success_url = reverse_lazy('unidade_list')
    
    def get_template_names(self):
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return ['unidades/unidade_form_modal.html']
        return ['unidades/unidade_form.html']
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        
        if form.is_valid():
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                form.save()
                return JsonResponse({'success': True})
            else:
                return self.form_valid(form)
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                html = render_to_string('unidades/unidade_form_modal.html', {'form': form, 'object': self.object}, request=request)
                return JsonResponse({'success': False, 'form_html': html})
            else:
                return self.form_invalid(form)

class UnidadeDelete(DeleteView):
    model = UnidadeAdministrativa
    template_name = 'unidades/unidade_confirm_delete.html'
    success_url = reverse_lazy('unidade_list')
    
    def get_template_names(self):
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return ['unidades/unidade_confirm_delete_modal.html']
        return ['unidades/unidade_confirm_delete.html']
    
    def post(self, request, *args, **kwargs):
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            self.object = self.get_object()
            self.object.delete()
            return JsonResponse({'success': True})
        else:
            return self.delete(request, *args, **kwargs)
