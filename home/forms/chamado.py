from django import forms
from ..models import Chamado
from django.utils.timezone import localtime


class ChamadoForm(forms.ModelForm):
    data_abertura_display = forms.DateTimeField(label='Data de Abertura', required=False, widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    data_fechamento_display = forms.DateTimeField(label='Data de Fechamento', required=False, widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    class Meta:
        model = Chamado
        fields = ['descricao', 'funcionario_abriu', 'funcionario_fechou', 'setor', 'descricao_solucao', 'data_fechamento_display', 'status']
        field_order = ['descricao', 'funcionario_abriu', 'funcionario_fechou', 'setor', 'descricao_solucao', 'data_abertura_display', 'data_fechamento_display',  'status']
        widgets = {
            'descricao': forms.Textarea(attrs={'rows': 3}),
            'descricao_solucao': forms.Textarea(attrs={'rows': 3}),
        }
        labels = {
            'descricao': 'Descrição do Chamado',
            'funcionario_abriu': 'Funcionário que Abriu',
            'funcionario_fechou': 'Funcionário que Fechou',
            'setor': 'Setor Responsável',
            'status': 'Status do Chamado',
            'descricao_solucao': 'Descrição da Solução',
            'data_fechamento_display': 'Data de Fechamento',
        }

    def __init__(self, *args, **kwargs):
        super(ChamadoForm, self).__init__(*args, **kwargs)

        self.fields['funcionario_abriu'].required = False

        if self.instance and self.instance.pk:
            self.fields['data_abertura_display'].initial = localtime(self.instance.data_abertura).strftime('%d/%m/%y %H:%M')
        if self.instance.data_fechamento:
            self.fields['data_fechamento_display'].initial = localtime(self.instance.data_fechamento).strftime('%d/%m/%y %H:%M')
        else:
            self.fields['data_fechamento_display'].initial = ''
