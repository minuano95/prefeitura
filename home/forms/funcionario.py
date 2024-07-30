from django import forms
from ..models import Funcionario
from phonenumber_field.formfields import PhoneNumberField

class FuncionarioForm(forms.ModelForm):
    telefone = PhoneNumberField(
        region='BR',
        error_messages={'invalid': 'Digite um número de telefone válido (por exemplo, (17) 99765-6789) ou um número com prefixo de chamada internacional.'}
    )

    class Meta:
        model = Funcionario
        fields = ['nome', 'cpf', 'telefone', 'setor', 'area_setor', 'nivel']

    def __init__(self, *args, **kwargs):
        user_level = kwargs.pop('user_level', None)
        super().__init__(*args, **kwargs)
        self.fields['nome'].widget.attrs.update({'class': 'funcionario-form'})
        self.fields['cpf'].widget.attrs.update({'class': 'funcionario-form'})
        self.fields['telefone'].widget.attrs.update({'class': 'funcionario-form'})
        self.fields['setor'].widget.attrs.update({'class': 'funcionario-form'})
        self.fields['area_setor'].widget.attrs.update({'class': 'funcionario-form'})
        self.fields['nivel'].widget.attrs.update({'class': 'funcionario-form'})

        if user_level != 'adm_sistema':
            self.fields['nivel'].choices = [
                ('adm', 'Administrador do Setor'),
                ('funcionario', 'Funcionário'),
            ]

    def clean(self):
        cleaned_data = super().clean()

        nome = cleaned_data.get('nome')
        if len(nome) == 0:
            raise forms.ValidationError('Este campo não pode ficar em branco.')
        elif len(nome)     > 100:
            raise forms.ValidationError('O nome não pode ter mais de 100 caracteres.')
        
        return cleaned_data
