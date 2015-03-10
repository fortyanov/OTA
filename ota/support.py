# -*- coding: utf-8 -*-
import codecs
from ota.errors import WrongAuthorisation, ServerDown, Exception403

__author__ = 'Fedor'
# СОДЕРЖИТ ДОПОЛНИТЕЛЬНЫЕ ЭЛЕМЕНТЫ НЕОБХОДИМЫЕ ДЛЯ РАБОТЫ С СОДЕРЖИМЫМ СЕРВАКА, ЧТОБЫ НЕ ФЛУДИТЬ ВО view.py

import fabric.contrib.files as ff
import time
import sys
import os
from ota_proj.settings import CORE_PATH, PROJECT_PATH
sys.path.append(CORE_PATH)
import shutil
import requests
import json
from errors import *
from ota.models import Document


DOC_DIR = os.path.join(PROJECT_PATH, 'media/documents')
SETTINGS_DIR = os.path.join(PROJECT_PATH, 'media/documents/settings')
FILES_DIR = os.path.join(PROJECT_PATH, 'media/documents/ts_files')
DOWNLOADED_DIR = os.path.join(PROJECT_PATH, 'media/documents/downloaded')

REMOTE_SETTINGS_DIR = '/opt/emercom/'
REMOTE_FILES_DIR = '/var/www/v3/pdg_emercom/carousel/'
REMOTE_SERVER_GEN_PORT = '8804'


def post(addr, action, data):
    """
    Генерит пост запросы
    """
    url = "%s%s" % (addr, action)
    # raise Exception(data)
    try:
        args = json.dumps(data)
        args = args.replace("+", "\\u002B")
        r = requests.post(url, data=args)
        print(r.text)
    except:
        raise ServerDown(u"Генератор не отвечает")
    if r.status_code == 200:
        return r.json()
    elif r.status_code == 403:
        print(r.text)
        raise Exception403(r.json()['dsc'].encode("utf8"))
    else:
        raise ServerDown(u"Генератор не отвечает [%s, %s]" % (url, r.status_code))


def clean_documents():
    """
    Чистит содержимое папок куда заливаются пользовательские файлы
    """
    path_to_documents = os.path.join(PROJECT_PATH, 'media/documents')
    if os.path.exists(path_to_documents):
        print('Old input files will be deleted!')
        print(path_to_documents)
        shutil.rmtree(path_to_documents)


def create_ts(selected_files):
    """
    Коннектится к серверу, закидывает pdg и файлы прошивки, создает ota файл, отсылает запрос на создание ts файла
    """
    pdg_setting_path = os.path.join(SETTINGS_DIR, 'pdg_setting')
    ota_setting_path = os.path.join(SETTINGS_DIR, 'ota_setting')
    selected_files_path = [os.path.join(FILES_DIR, f) for f in selected_files]
    server_setting_data = json.load(open(os.path.join(SETTINGS_DIR, 'server_setting.json')))

    ########### создание ota_setting #############
    generated_ota_data = u'\n'
    for i, f in enumerate(selected_files, start=1):
        generated_ota_data += u"    Module(  INPUT=path+\"%s\",      moduleId = %s, moduleVersion = 0x01, descriptors = [name_descriptor(name='%s')],),\n" % (f, hex(i), 100 + i)
    with codecs.open(ota_setting_path, 'w', encoding="utf8") as ota_setting:
        ota_setting.write(u'# OTA setting file\n'
                          u'#Input file  attributes here\n'
                          u'# START                file_name         file_number          version                           description\n'
                          u'self.modules2 = [%s]\n' % generated_ota_data)
    ##############################################

    ff.env['abort_on_prompts'] = True              # в случае требования ручного ввода чего либо в коммандной строке удаленного сервака (у нас это возможно только в случае некорректности логина/пароля), будет выскакивать ошибка
    host_string = "%s@%s" % (server_setting_data['server_user'], server_setting_data['server_addr'])
    if server_setting_data['server_port']:
        host_string += ':%s' % server_setting_data['server_port']

    try:
        with ff.settings(user=server_setting_data['server_user'], password=server_setting_data['server_pass'],
                         host_string=host_string):
            ff.env['sudo_user'] = 'root'    # указывает из под какого пользователя выполнять use_sudo

            print('pdg_setting-exists: %s' % os.path.exists(pdg_setting_path))
            # print('pdg_setting_path: %s' % pdg_setting_path)
            if os.path.exists(pdg_setting_path):
                ff.put(remote_path=REMOTE_SETTINGS_DIR, local_path=pdg_setting_path, use_sudo=True)
                ff.sudo('supervisorctl restart emercom_ota', user='root')                       # перезапуск генератора необходим после каждогого изменения в pdg_setting
                time.sleep(5)

            ff.put(remote_path=REMOTE_SETTINGS_DIR, local_path=ota_setting_path, use_sudo=True)

            ff.sudo('rm -f %s*' % REMOTE_FILES_DIR, user='root')                                # очистка списка файлов (user='root' и ff.env['sudo_user'] = 'root';  ...use_sudo=True это 2 способа для получения рутовых прав на bash команды обращенные к серверу)
            for one_file_path in selected_files_path:
                ff.put(remote_path=REMOTE_FILES_DIR, local_path=one_file_path, use_sudo=True)   # для put и get работает только use_sudo=True
    except:
        raise WrongAuthorisation(u'Ошибка при взаимодействии с сервером. Проверьте логин-пароль')

    remote_url = 'http://%s:%s/' % (server_setting_data['server_addr'], REMOTE_SERVER_GEN_PORT)
    post(remote_url, 'dsmcc_generate', {})


def download_from_remote(remote_file_path='/opt/emercom/pdg_setting'):
    """
        Коннектится к серверу, отправляет файл с настройками из сервера(/opt/emercom/pdg_setting)
        на локальное хранилище (ota_web/media/documents/downloaded)
        с целью последуещей выгрузки через браузер пользователя.
    """
    if not os.path.exists(DOWNLOADED_DIR):
        os.mkdir(DOWNLOADED_DIR)

    try:
        server_setting_data = json.load(open(os.path.join(SETTINGS_DIR, 'server_setting.json')))
    except IOError:
        raise WrongServerSetting(u'Файл настроек сервера отсутствует или некорректен.')

    ff.env['abort_on_prompts'] = True
    host_string = "%s@%s" % (server_setting_data['server_user'], server_setting_data['server_addr'])
    if server_setting_data['server_port']:
        host_string += ':%s' % server_setting_data['server_port']
    try:
        with ff.settings(user=server_setting_data['server_user'], password=server_setting_data['server_pass'],
                         host_string=host_string):

            ff.get(local_path=DOWNLOADED_DIR, remote_path=remote_file_path)
            res_path = os.path.join(DOWNLOADED_DIR, os.path.split(remote_file_path)[1])
            print(res_path)
            return res_path         # на выход формируется локальный путь куда загрузился файл

    except:
        raise WrongAuthorisation(u'Ошибка при авторизации на сервер')


def get_pdg_status():
    """
    Коннектится к серверу собирает данные о статусе генератора
    """
    try:
        server_setting_data = json.load(open(os.path.join(SETTINGS_DIR, 'server_setting.json')))
    except IOError:
        raise WrongServerSetting(u'Файл настроек сервера отсутствует или некорректен.')

    ff.env['abort_on_prompts'] = True
    host_string = "%s@%s" % (server_setting_data['server_user'], server_setting_data['server_addr'])
    if server_setting_data['server_port']:
        host_string += ':%s' % server_setting_data['server_port']

    try:
        with ff.settings(user=server_setting_data['server_user'], password=server_setting_data['server_pass'],
                         host_string=host_string):
            data = ff.sudo('supervisorctl status', user="root").split("\r\n")
            for i, line in enumerate(data):
                formatted_data = filter(lambda x: x != '', line.split(" "))                        # рубим строку по пробелам и если пробелов много появляются элементы содержащие '', filter убирает их спомошью лямбда-функции
                if formatted_data[0] == 'emercom_ota':
                    return formatted_data[1]
    except:
        raise WrongAuthorisation(u'Ошибка при авторизации на сервер')


def get_dsmcc_status():
    try:
        server_setting_data = json.load(open(os.path.join(SETTINGS_DIR, 'server_setting.json')))
    except IOError:
        raise WrongServerSetting(u'Файл настроек сервера отсутствует или некорректен.')

    remote_url = 'http://%s:%s/' % (server_setting_data['server_addr'], REMOTE_SERVER_GEN_PORT)
    return post(remote_url, 'dsmcc_status', {})


def broadcast(broadcast_status):
    """
    Отсылает запросы для запуска/остановки подмешивания ts файла
    """
    server_setting_data = json.load(open(os.path.join(SETTINGS_DIR, 'server_setting.json')))
    remote_url = 'http://%s:%s/' % (server_setting_data['server_addr'], REMOTE_SERVER_GEN_PORT)
    if broadcast_status == 'start':
        return post(remote_url, 'dsmcc_start', {})
    if broadcast_status == 'stop':
        return post(remote_url, 'dsmcc_stop', {})


def create_doc_dir():
    """
    Создает хранилише для используемых документов (файлов прошивки и настроек)
    """
    if not os.path.exists(DOC_DIR):
        os.makedirs(DOC_DIR)
    if not os.path.exists(SETTINGS_DIR):
        os.mkdir(SETTINGS_DIR)
    if not os.path.exists(FILES_DIR):
        os.mkdir(FILES_DIR)


def set_server(setting):
    """
    Сохранение настроек сервера в виде json
    """
    create_doc_dir()
    json.dump(setting, open(os.path.join(SETTINGS_DIR, 'server_setting.json'), 'wb'), indent=4)

def get_server():
    """
    Получение настроек сервера в виде json
    """
    server_setting_path = os.path.join(SETTINGS_DIR, 'server_setting.json')
    if os.path.exists(server_setting_path):
        fields_data = json.load(open(server_setting_path))
        if fields_data['server_port'] != None:
            fields_data['server_addr'] = 'http://' + fields_data['server_addr'] + ':' + fields_data['server_port']
        else:
            fields_data['server_addr'] = 'http://' + fields_data['server_addr']
    else:
        fields_data = {"server_addr": u"http://адрес сервера:порт", "server_user": u"логин"}
    return fields_data

def set_pdg(pdg_file):
    """
    Сохранение настроек генератора
    """
    create_doc_dir()
    pdg_setting_path = os.path.join(SETTINGS_DIR, 'pdg_setting')
    if os.path.exists(pdg_setting_path):
        os.remove(pdg_setting_path)

    pdg_file, new = Document.objects.get_or_create(pdg_file=pdg_file)
    print(pdg_file, new)
    pdg_file.save()


def edit_pdg(pdg_file_data):
    """
    Изменение и сохранение настроек генератора
    """
    create_doc_dir()
    pdg_setting_path = os.path.join(SETTINGS_DIR, 'pdg_setting')
    if os.path.exists(pdg_setting_path):
        os.remove(pdg_setting_path)

    with codecs.open(pdg_setting_path, 'w', encoding="utf8") as f:
        f.write(pdg_file_data)


def get_file_data(inp_file):
    """
    Получение содержимого файла
    """
    inp_file_path = os.path.join(SETTINGS_DIR, inp_file)
    with open(inp_file_path) as f:
        res = f.read()
    return res


def set_files(files):
    """
    Сохранение списка файлов (путь указан в модели Document)
    """
    for f in files:
        ts_doc = Document(ts_files=f)
        ts_doc.save()


def get_all_files():
    """
    Получение списка имен файлов (дирректория FILES_DIR)
    """
    create_doc_dir()
    ts_files = os.listdir(FILES_DIR)
    ts_files.sort()
    return ts_files


def del_files(files):
    """
    Удаление файлов по именам (дирректория FILES_DIR)
    """
    for f in files: os.remove(os.path.join(FILES_DIR, f))