# -*- coding: utf-8 -*-

import os
import re
import json
import magic

from django import forms
from django.conf import settings

from django.utils.html import mark_safe

from utils import format_file_extensions

from ajax_upload.widgets import AjaxClearableFileInput


class MultiuploadWidget(forms.MultipleHiddenInput):
    def __init__(self, attrs={}):
        super(MultiuploadWidget, self).__init__(attrs)

    def render(self, name, value, attrs=None, choices=()):
        widget_ = super(MultiuploadWidget, self).render(name, value, attrs)
        output = '<div id="hidden_container" style="display:none;">%s</div>' % widget_
        return mark_safe(output)


class MultiuploaderField(forms.MultiValueField):
    widget = MultiuploadWidget()

    def formfield(self, **kwargs):
        kwargs['widget'] = MultiuploadWidget
        return super(MultiuploaderField, self).formfield(**kwargs)

    def validate(self, values):
        super(MultiuploaderField, self).validate(values)

    def clean(self, values):
        super(MultiuploaderField, self).clean(values)
        return values

    def compress(self, value):
        if value:
            return value

        return None


class MultiUploadForm(forms.Form):
    file = forms.FileField(label=u'Добавить', widget=AjaxClearableFileInput())

    def __init__(self, *args, **kwargs):
        multiuploader_settings = getattr(settings, "MULTIUPLOADER_FORMS_SETTINGS")
        form_type = kwargs.pop("form_type", "default")

        options = {
            'maxFileSize': multiuploader_settings[form_type]["MAX_FILE_SIZE"],
            'acceptFileTypes': format_file_extensions(multiuploader_settings[form_type]["FILE_TYPES"]),
            'maxNumberOfFiles': multiuploader_settings[form_type]["MAX_FILE_NUMBER"],
            'allowedContentTypes': map(str.lower, multiuploader_settings[form_type]["CONTENT_TYPES"]),
            'autoUpload': multiuploader_settings[form_type]["AUTO_UPLOAD"]
        }

        self.check_extension = False
        self.check_content_type = False
        # self.check_english_name = True

        if multiuploader_settings[form_type]["FILE_TYPES"] == '*':
            self.check_extension = False
            options.update({'acceptFileTypes': []})

        if multiuploader_settings[form_type]["CONTENT_TYPES"] == '*':
            self.check_content_type = False
            options.pop('allowedContentTypes')

        self._options = options
        self.options = json.dumps(options)

        super(MultiUploadForm, self).__init__(*args, **kwargs)

        self.fields["file"].widget = forms.FileInput(attrs={'multiple': True})

    def clean_file(self):
        #print('cleaned_data: %s' % self.cleaned_data)
        content = self.cleaned_data[u'file']
        #print(self.data)
        #print(self.data['file'])
        filename, extension = os.path.splitext(content.name)
        #print('content: %s' % content)

        if self.check_extension:
            if re.match(self._options['acceptFileTypes'], extension, flags=re.I) is None:
                raise forms.ValidationError(u"Файлы без разрешений не поддерживаются")

        if self.check_content_type:
            content_type = magic.from_buffer(content.read(1024), mime=True)
            if content_type.lower() in self._options['allowedContentTypes']:
                if content._size > self._options['maxFileSize']:
                    raise forms.ValidationError(u"Превышен максимальный размер одного из файлов")
            else:
                raise forms.ValidationError(u"Недопустимое содержимое файлов")

        # if self.check_english_name:
        #     try:
        #         print('filename: %s - %s' % (str(filename), type(filename)))
        #         #print('content: %s - %s' % (str(content), type(content)))
        #     except UnicodeEncodeError:
        #         raise forms.ValidationError(u"Названия файлов могут содержать только латиницу")

        return content


class MultiuploaderMultiDeleteForm(forms.Form):
    id = MultiuploaderField()
