# -*- coding: utf-8 -*-
"""
    Интерфейс для управления OTA

    .. codeauthor:: Fedor Ortyanov <f.ortyanov@roscryptpro.ru> , Alexey Nabrodov <a.nabrodov@roscryptpro.ru>
"""

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import auth
import json
import os
from ota.forms import LoginForm, ServerSettingForm, AddUserForm, PDG_Form
from django.shortcuts import render_to_response, HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from ota.multiuploader.forms import MultiUploadForm
import ota.support as sup
from errors import WrongAuthorisation, ServerDown, WrongServerSetting
from django.contrib import messages


def login(request):
    login_form_errors = {}
    if request.method == 'GET':
        login_form = LoginForm()
    else:
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            cd = login_form.cleaned_data
            username = cd['login']
            password = cd['password']
            user = auth.authenticate(username=username, password=password)
            if user is not None and user.is_active:
                auth.login(request, user)
                if user.is_staff: return HttpResponseRedirect("/staff/control/")
                else:             return HttpResponseRedirect("/operator/control/")
            else:
                login_form._errors["login"] = login_form.error_class([u'Ошибка при авторизации'])
        login_form_errors = {field: login_form._errors[field].as_text()[2:] for field in login_form._errors}

    return render_to_response('login.html', {'login_form_errors': login_form_errors}, context_instance=RequestContext(request))


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/accounts/login/")


@login_required
@staff_member_required
def admin_control(request):
    return render_to_response('admin_control.html', context_instance=RequestContext(request))


@login_required
@staff_member_required
def admin_set_server(request):
    serv_form_errors = {}
    saved = False
    server_port = None

    if request.method == 'GET':
        serv_form = ServerSettingForm()
    else:
        serv_form = ServerSettingForm(request.POST)
        if serv_form.is_valid():
            # try:
            cleaned_server_addr = request.POST[u'server_addr'].split('/')[2]
            print('cleaned_server_addr: %s' % cleaned_server_addr)
            if ':' in cleaned_server_addr:
                server_port = cleaned_server_addr.split(':')[1]
                cleaned_server_addr = cleaned_server_addr.split(':')[0]
            server_user = request.POST[u'server_user']
            server_pass = request.POST[u'server_pass']
            setting = {'server_addr': cleaned_server_addr, 'server_user': server_user, 'server_pass': server_pass, 'server_port': server_port}
            sup.set_server(setting)
            saved = True
            # except IndexError:
                    # serv_form._errors[u'server_addr'] = serv_form.error_class([u'Некорректный адрес сервера'])
        serv_form_errors = {field: serv_form._errors[field].as_text()[2:] for field in serv_form._errors}        # Изврат для получения словаря, содержащего строки с ошибками по ключам-полям формы
    fields_data = sup.get_server()

    return render_to_response('admin_set_server.html', {'fields_data': fields_data, 'serv_form_errors': serv_form_errors, "saved": saved}, context_instance=RequestContext(request))


@login_required
@staff_member_required
def admin_set_pdg(request):
    print('request.POST: %s' % request.POST)
    print('request.FILES: %s' % request.FILES)
    saved = False
    pdg_form_errors = {}
    if request.method == 'GET':
        pdg_form = PDG_Form()
    else:
        pdg_form = PDG_Form(request.POST, request.FILES)
        print('pdg_form.is_valid: %s' % pdg_form.is_valid())
        if pdg_form.is_valid() and u'pdg_file' in request.FILES:
            pdg_file = request.FILES.get(u'pdg_file')
            sup.set_pdg(pdg_file)
            saved = True
        pdg_form_errors = {field: pdg_form._errors[field].as_text()[2:] for field in pdg_form._errors}
    return render_to_response('admin_set_pdg.html', {'pdg_form_errors': pdg_form_errors, "saved": saved}, context_instance=RequestContext(request))


@login_required
@staff_member_required
def admin_edit_pdg(request):
    if request.POST.get(u'code', ''):
        pdg_file_data = request.POST.get(u'code', '')
        sup.edit_pdg(pdg_file_data)
    try:
        pdg_file_data = sup.get_file_data('pdg_setting')
    except IOError:
        pdg_file_data = u'Вероятно, файл отсутствует'
    return render_to_response('admin_edit_pdg.html', {'pdg_file_data': pdg_file_data}, context_instance=RequestContext(request))


@login_required
@staff_member_required
def download_pdg_file(request):
    try:
        file = open(sup.download_from_remote(remote_file_path='/opt/emercom/pdg_setting'), 'rb')
        response = HttpResponse(file, mimetype='application/force-download')
        response['Content-Disposition'] = 'attachment; filename="pdg_setting"'
    except WrongServerSetting:
        html = "<html><body>Файл настроек сервера отсутствует на сервере, скачивание невозможно.</body></html>"
        response = HttpResponse(html)
    except WrongAuthorisation:
        html = "<html><body>Неправильные настройки подключеня или на сервере отсутствует файл с настройкми, скачивание невозможно.</body></html>"
        response = HttpResponse(html)
    return response


@login_required
@staff_member_required
def admin_add_user(request):
    print('request.POST: %s' % request.POST)
    saved = False
    user_form_errors = {}
    if request.method == 'GET':
        user_form = AddUserForm()
    else:
        user_form = AddUserForm(request.POST)
        if user_form.is_valid():
            try:
                user = User.objects.create(username=request.POST[u'login'])
                user.set_password(request.POST[u'password'])
                user.save()
                saved = True
            except:                            #дописать тип ошибки
                user_form._errors[u'login'] = user_form.error_class([u'Невозможно создать существующего пользователя'])
        user_form_errors = {k: user_form._errors[k].as_text()[2:] for k in user_form._errors.keys()}        # Изврат для получения словаря, содержащего строки с ошибками по ключам-полям формы

    return render_to_response('admin_add_user.html', {"saved": saved, "user_form_errors": user_form_errors}, context_instance=RequestContext(request))


@login_required
@staff_member_required
def admin_del_user(request):
    print('request.POST: %s' % request.POST)
    if u'users_names[]' in request.POST:
        selected_users = request.POST.getlist(u'users_names[]')
        for one_user in selected_users:
            User.objects.get(username=one_user).delete()

    all_users = User.objects.all()
    all_users_names = [one_user.username for one_user in all_users if not one_user.is_staff]
    return render_to_response('admin_del_user.html', {'all_users': all_users_names}, context_instance=RequestContext(request))


@login_required
def operator_control(request):
    return render_to_response('operator_control.html', context_instance=RequestContext(request))


@login_required
def operator_set_files(request):
    print('request.POST: %s' % request.POST)
    print('request.FILES: %s' % request.FILES)
    saved = False
    upload_form_errors = {}

    if request.method == 'GET':
        upload_from = MultiUploadForm()
    else:
        upload_form = MultiUploadForm(request.POST, request.FILES)
        if upload_form.is_valid():
            files = request.FILES.getlist(u'file')
            try:
                for f in files:
                    print(str(unicode(f)))
                saved = True
            except UnicodeEncodeError:
                upload_form._errors["file"] = upload_form.error_class([u"Названия файлов не могут содержать кириллицу."])
                files = []
            sup.set_files(files)
        upload_form_errors = {field: upload_form._errors[field].as_text()[2:] for field in upload_form._errors}

    all_files = sup.get_all_files()
    return render_to_response('operator_set_files.html', {'upload_form_errors': upload_form_errors, "saved": saved, "all_files": all_files}, context_instance=RequestContext(request))


@login_required
def operator_del_files(request):
    if u'files_names[]' in request.POST:
        selected_files = request.POST.getlist(u'files_names[]')
        sup.del_files(selected_files)
    all_files = sup.get_all_files()
    return render_to_response('operator_del_files.html', {'all_files': all_files}, context_instance=RequestContext(request))


@login_required
def operator_create_ts(request):
    print('request.POST: %s' % request.POST)
    if u'files_names[]' in request.POST:
        selected_files = request.POST.getlist(u'files_names[]')
        try:
            sup.create_ts(selected_files)
            return HttpResponse(json.dumps({"success": True, "msg": u'Поток успешно создан'}))
        except WrongAuthorisation:
            return HttpResponse(json.dumps({"success": False, "msg": u'Ошибка при взаимодействии с сервером. Проверьте корректность установленного генератора.'}))
    all_files = sup.get_all_files()
    return render_to_response('operator_create_ts.html', {'all_files': all_files}, context_instance=RequestContext(request))


@login_required
def operator_broadcast(request):
    pdg_status = broadcast_status = generate_status = u'НЕИЗВЕСТНО'
    if u'broadcast_status' in request.POST:
        if request.POST[u'broadcast_status'] == 'start':
            sup.broadcast(broadcast_status='start')
        if request.POST[u'broadcast_status'] == 'stop':
            sup.broadcast(broadcast_status='stop')

    try:
        pdg_status = sup.get_pdg_status()
        print('pdg_status: %s' % pdg_status)
        if pdg_status == 'RUNNING': pdg_status = u'ЗАПУЩЕНО'
        if pdg_status == 'STOPPED': pdg_status = u'ОСТАНОВЛЕНО'

        dsmcc_status = sup.get_dsmcc_status()
        generate_status = dsmcc_status[u'reply'][u'generate_dsmcc']
        if dsmcc_status[u'reply'][u'send_dsmcc'] == 1:
            broadcast_status = u'ЗАПУЩЕНО'
        elif dsmcc_status[u'reply'][u'send_dsmcc'] == 0:
            broadcast_status = u'ОСТАНОВЛЕНО'
    except WrongAuthorisation:
        messages.error(request, u'Ошибка подключения к удаленному серверу, сообщите о неполадке администратору.')
    except ServerDown:
        broadcast_status = u'ОСТАНОВЛЕНО'              # чтобы при невозможности получения статуса трансляции она отображалась как остановленная (НЕИЗВЕСТНО - не корректно)
    except WrongServerSetting:
        messages.error(request, u'Файл настроек сервера отсутствует или некорректен.')

    return render_to_response('operator_broadcast.html', {
        'pdg_status': pdg_status,
        'broadcast_status': broadcast_status,
        'generate_status': generate_status,
        'saved': True if "success" in request.GET else False
    }, context_instance=RequestContext(request))


@login_required
def operator_broadcast_first(request):                        # Фейковая вьюха, нужна чтобы что то показывать пользователю в тот момент когда выполняется основная вьюха, содержащая логику и отрисовку данных
    return render_to_response('operator_broadcast_first.html')


@login_required
def hello(request):
    return render_to_response('hello.html', context_instance=RequestContext(request))



