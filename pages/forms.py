from django import forms
from django.conf import settings
from django.core.mail import send_mail

class ContactForm(forms.Form):
    email = forms.EmailField()
    ativo = forms.CharField(max_length=15)
    condition = forms.ChoiceField(choices=[('passar de', 'passar de'), ('cair de', 'cair de')])
    price = forms.CharField(max_length=70)

    def get_info(self):
        """
        Method that returns formatted information
        :return: subject, msg
        """
        # Cleaned data
        cl_data = super().clean()

        from_email = cl_data.get('email')
        ativo = cl_data.get('ativo')
        condition = cl_data.get('condition')
        price = cl_data.get('price')

        if(condition == "passar de"):
            msg = f'\nO valor do ativo {ativo} está mais caro que {price}$, é melhor vender!'
        else:
            msg = f'\nO valor do ativo {ativo} está mais barato que {price}$, é hora de comprar!'

        return ativo, msg, from_email

    def send(self):
        
        subject, msg, email = self.get_info()

        send_mail(
            subject=f'Ativo - {subject}',
            message=msg,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email]
        )