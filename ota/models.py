# -*- coding: utf-8 -*-
from django.db import models


class Document(models.Model):
    pdg_file = models.FileField(upload_to='documents/settings')                 # Путь относительно settings.MEDIA_ROOT
    ota_file = models.FileField(upload_to='documents/settings')
    ts_files = models.FileField(upload_to='documents/ts_files')

