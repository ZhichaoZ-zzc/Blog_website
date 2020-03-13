from django.core.exceptions import ValidationError

from django import forms as django_forms
from .base import BaseForm
from django.forms import fields as django_fields


class LoginForm(BaseForm, django_forms.Form):
    username = django_fields.CharField()
    password = django_fields.CharField()
    rmb = django_fields.IntegerField(required=False)
    check_code = django_fields.CharField(
        error_messages={'required': '验证码不能为空.'}
    )

    def clean_check_code(self):   #有个钩子
        if self.request.session.get('CheckCode').upper() != self.request.POST.get('check_code').upper():
            raise ValidationError(message='验证码错误', code='invalid')

