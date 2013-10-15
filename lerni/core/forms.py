# coding: utf-8

from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User
from lerni.core.models import Teacher
from django.utils.translation import ugettext as _
from django.core.exceptions import ObjectDoesNotExist

class UserAddForm(ModelForm):

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password')

    check_password = forms.CharField(label=_('Confirme a Senha'), max_length=30, widget=forms.PasswordInput, required=True)

    def __init__(self, *args, **kwargs):

        #self.base_fields[''].label = _('')
        self.base_fields['first_name'].label = _('Nome')
        self.base_fields['last_name'].label = _('Sobrenome')
        self.base_fields['email'].label = _('Email')
        self.base_fields['password'].label = _('Senha')
        self.base_fields['username'].label = _(u'Usuário')

        self.base_fields['password'].help_text = 'Informe uma senha segura'
        self.base_fields['password'].widget = forms.PasswordInput()
        self.base_fields['first_name'].required = True

        self.base_fields['last_name'].required = True
        self.base_fields['email'].required = True

        super(UserAddForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):

        #Salva o usuario mas não faz alteração no bd
        user = super(UserAddForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])

        if commit:
            #Agora faz alteração no db

            user.save()

        return user

    def clean_first_name(self):
        self.cleaned_data['first_name'] = self.cleaned_data['first_name'].title()
        return self.cleaned_data['first_name']

    def clean_last_name(self):
        self.cleaned_data['last_name'] = self.cleaned_data['last_name'].title()
        return self.cleaned_data['last_name']

    def clean_username(self):
        if User.objects.filter(username=self.cleaned_data['username'],).count():
            raise forms.ValidationError(u'Este usuário já foi cadastrado!')

        return self.cleaned_data['username']

    def clean_password(self):

        if len(self.cleaned_data['password']) < 6:
            raise forms.ValidationError(u"Sua senha deve ter no mínimo 6 caracteres!")
        return self.cleaned_data['password']

    def clean_check_password(self):
        if self.cleaned_data['check_password'] != self.data['password']:
            raise forms.ValidationError(u"Senhas não correspondem!")
        return self.cleaned_data['check_password']


class UserUpdateForm(ModelForm):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email','username')

    def __init__(self, *args, **kwargs):

        #self.base_fields[''].label = _('')
        self.base_fields['first_name'].label = _('Nome')
        self.base_fields['last_name'].label = _('Sobrenome')
        self.base_fields['email'].label = _('Email')
        self.base_fields['username'].label = _(u'Usuário')

        self.base_fields['first_name'].required = True
        self.base_fields['last_name'].required = True
        self.base_fields['email'].required = True
        self.base_fields['username'].required = True


        super(UserUpdateForm, self).__init__(*args, **kwargs)

    def clean_first_name(self):
        self.cleaned_data['first_name'] = self.cleaned_data['first_name'].title()
        return self.cleaned_data['first_name']

    def clean_last_name(self):
        self.cleaned_data['last_name'] = self.cleaned_data['last_name'].title()
        return self.cleaned_data['last_name']

    def clean_username(self):

        try:

            userFiltered = User.objects.filter(username=self.cleaned_data['username']).get()

        except ObjectDoesNotExist:

            return self.cleaned_data['username']

        user = super(UserUpdateForm, self).save(commit=False)

        if userFiltered.id != user.id:
            raise forms.ValidationError(u'Este usuário já foi cadastrado!')

        return self.cleaned_data['username']



