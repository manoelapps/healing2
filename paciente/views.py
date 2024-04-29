# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from medico.models import DadosMedico, Especialidades, DatasAbertas, is_medico
from datetime import datetime
from django.contrib.messages import constants
from django.contrib import messages
import locale
from .models import Consulta, Documento, Avaliacoes
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.db import transaction

# Create your views here.
@login_required
def home(request):
    if request.method == "GET":
        medico_filtrar = request.GET.get('medico')
        especialidades_filtrar = request.GET.getlist('especialidades')
        medicos = DadosMedico.objects.all()

        consultas = Consulta.objects.filter(paciente=request.user).filter(status = 'A')
        minhas_consultas = Consulta.objects.filter(paciente=request.user).filter(data_aberta__data__gte=datetime.now()).exclude(status='C').order_by('data_aberta__data')
        #dado_medico = [consulta.data_aberta.user for consulta in minhas_consultas]

        if medico_filtrar:
            medicos = medicos.filter(nome__icontains=medico_filtrar)
        
        if especialidades_filtrar:
            medicos = medicos.filter(especialidade_id__in=especialidades_filtrar)

        especialidade = Especialidades.objects.all()
        return render(request, 'home.html', {'medicos': medicos, 'minhas_consultas': minhas_consultas,'consultas': consultas, 'especialidades': especialidade, 'is_medico': is_medico(request.user)})
    
@login_required
def escolher_horario(request, id_dados_medicos):
    if request.method == "GET":
        medico = DadosMedico.objects.get(id=id_dados_medicos)
        datas_abertas = DatasAbertas.objects.filter(user=medico.user).filter(data__gte=datetime.now()).filter(agendado=False).order_by('data')
        return render(request, 'escolher_horario.html', {'medico': medico, 'datas_abertas': datas_abertas, 'is_medico': is_medico(request.user)})

@login_required
@transaction.atomic
def agendar_horario(request, id_data_aberta):
    if request.method == "GET":
        data_aberta = DatasAbertas.objects.get(id=id_data_aberta)

        horario_agendado = Consulta(
            paciente=request.user,
            data_aberta=data_aberta,
        )
        
        horario_agendado.save()

        # TODO: Sugestão Tornar atomico

        data_aberta.agendado = True
        data_aberta.save()

        messages.add_message(request, constants.SUCCESS, 'Horário agendado com sucesso.')

        return redirect('/pacientes/minhas_consultas/')

@login_required   
def minhas_consultas(request):
    if request.method == "GET":
        minhas_consultas = Consulta.objects.filter(paciente=request.user).filter(data_aberta__data__gte=datetime.now()).exclude(status='C').order_by('data_aberta__data')
        consultas_iniciadas = minhas_consultas.filter(status='I')
        consultas_anteriores = Consulta.objects.filter(paciente=request.user).filter(status='F' and 'S').order_by('data_aberta__data')
       # dado_medico = [consulta.data_aberta.user for consulta in minhas_consultas]
        return render(request, 'minhas_consultas.html', {'minhas_consultas': minhas_consultas,'consultas_iniciadas': consultas_iniciadas, 'consultas_anteriores': consultas_anteriores, 'is_medico': is_medico(request.user)})

@login_required
def sair(request):
    auth.logout(request)
    return redirect('/usuarios/login')

@login_required
def consulta(request, id_consulta):
    if request.method == 'GET':
        consulta = Consulta.objects.get(id=id_consulta)
        dado_medico = DadosMedico.objects.get(user=consulta.data_aberta.user)
        documentos = Documento.objects.filter(consulta=consulta)
        avaliacoes = Avaliacoes.objects.filter(consulta_id=id_consulta)
       
    
        print(avaliacoes)
        return render(request, 'consulta.html', {'consulta': consulta, 'dado_medico': dado_medico, 'documentos': documentos, 'avaliacoes': avaliacoes, 'is_medico': is_medico(request.user)})

@login_required
def cancelar_consulta(request, id_consulta):
    consulta = Consulta.objects.get(id=id_consulta)
    data_aberta = consulta.data_aberta
    
    if request.user != consulta.paciente:
        messages.add_message(request, constants.ERROR, 'Essa consulta nao e sua')
        return redirect('/pacientes/minhas_consultas/')

    
    consulta.status = 'C'
    consulta.save()

    data_aberta.agendado=False
    data_aberta.save()
    return redirect(f'/pacientes/consulta/{id_consulta}')

@login_required
def add_documento(request, id_consulta):

    if not is_medico(request.user):
        messages.add_message(request, constants.WARNING, 'Somente médicos podem acessar essa página.')
        return redirect('/usuarios/sair')
    
    consulta = Consulta.objects.get(id=id_consulta)
    
    if consulta.data_aberta.user != request.user:
        messages.add_message(request, constants.ERROR, 'Essa consulta não é sua!')
        return redirect(f'/medicos/consulta_area_medico/{id_consulta}')
    
    
    titulo = request.POST.get('titulo')
    documento = request.FILES.get('documento')

    if not documento:
        messages.add_message(request, constants.WARNING, 'Adicione o documento.')
        return redirect(f'/medicos/consulta_area_medico/{id_consulta}')

    documento = Documento(
        consulta=consulta,
        titulo=titulo,
        documento=documento

    )

    documento.save()

    messages.add_message(request, constants.SUCCESS, 'Documento enviado com sucesso!')
    return redirect(f'/medicos/consulta_area_medico/{id_consulta}')

def avaliacao_consulta(request, id_consulta):

    consulta = Consulta.objects.get(id=id_consulta)

    
    
    if request.method == 'POST':
        if request.user != consulta.paciente:
            messages.add_message(request, constants.WARNING, 'Apenas o paciente pode avaliar essa consulta!')
            return redirect('/pacientes/home/')
        
        
        consulta=Consulta.objects.get(id=id_consulta)
        avaliacao=request.POST.get('avaliacao')
        comentario=request.POST.get('comentario')   
        
    
        avaliacao = Avaliacoes(
        consulta=consulta,
        comentario=comentario,
        avaliacao= avaliacao
        )
        avaliacao.save()

        consulta.status = 'S'
        consulta.save()

        messages.add_message(request, constants.SUCCESS, 'Avaliação salva com sucesso')
        return redirect(f'/pacientes/consulta/{id_consulta}')
    
def hisrorico_consultas(request):
    if request.method == "GET":
        consultas_anteriores = Consulta.objects.filter(paciente=request.user).filter(status='F' and 'S').order_by('data_aberta__data')
        consultas_anteriores_c = Consulta.objects.filter(paciente=request.user).filter(status='C').order_by('data_aberta__data')
       
        return render(request, 'historico_consultas.html', {'consultas_anteriores': consultas_anteriores, 'consultas_anteriores_c': consultas_anteriores_c, 'is_medico': is_medico(request.user)})