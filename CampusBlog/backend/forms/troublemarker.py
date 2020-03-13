from django.forms import Form
from django.forms import fields
from django.forms import widgets

class TroubleMaker(Form):
    title = fields.CharField(
        max_length=32,
        widget=widgets.TextInput(attrs={'class': 'form-control'})
    )
    detail = fields.CharField(
        widget=widgets.Textarea(attrs={'id':'detail','class':'kind-content'})
    )


class TroubleKill(Form):
    """
    解决方案
    """

    solution = fields.CharField(
        widget=widgets.Textarea(attrs={'id':'solution','class':'kind-content'})
    )
