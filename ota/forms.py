#! coding: utf-8
from django import forms


class LoginForm(forms.Form):
    login = forms.CharField(label=u'Логин', max_length=15)
    password = forms.CharField(label=u'Пароль', max_length=15, widget=forms.PasswordInput)

#    helper = FormHelper()
#    helper.form_class = 'form-horisontal'
#    helper.layout = Layout(
#        Field(u'Логин', css_class='input-xxlarge'),
#        Field(u'Пароль', css_class='input-xxlarge')
#    )

    def clean_login(self):
        login = self.cleaned_data['login']
        if len(login) < 4:
            raise forms.ValidationError(u"Не менее 4 символов.")
        return login

    def clean_password(self):
        password = self.cleaned_data['password']
        if len(password) < 4:
            raise forms.ValidationError(u"Не менее 4 символов.")
        return password


class ServerSettingForm(forms.Form):
    server_addr = forms.URLField(label=u'Адрес сервера', initial='http://172.20.')
    server_user = forms.CharField(label=u'Логин', max_length=15, initial='root')
    server_pass = forms.CharField(label=u'Пароль', max_length=15, widget=forms.PasswordInput)


class PDG_Form(forms.Form):
    pdg_file = forms.FileField(label=u'Файл с настройками')

    def clean_pdg_file(self):
        pdg_file = self.cleaned_data['pdg_file']
        print('pdg_file: %s' % pdg_file)
        if str(pdg_file) != 'pdg_setting':
            raise forms.ValidationError(u"Возможна загрузка только файла pdg_setting.")
        return pdg_file


class AddUserForm(LoginForm):
    pass
