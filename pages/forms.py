from django import forms
from django.conf import settings
from django.core.mail import send_mail

class ContactForm(forms.Form):
    email = forms.CharField(max_length=70)
    stock = forms.CharField(max_length=70)
    condition = forms.CharField(max_length=70)
    price = forms.CharField(max_length=70)

    def get_info(self):
        """
        Method that returns formatted information
        :return: subject, msg
        """
        # Cleaned data
        cl_data = super().clean()

        from_email = cl_data.get('email')
        stock = cl_data.get('stock')
        condition = cl_data.get('condition')
        price = cl_data.get('price')

        if(condition == "passar de"):
            msg = f'\n"O valor do ativo {stock} está mais caro que {price}$, é melhor vender!"'
        else:
            msg = f'\n"O valor do ativo {stock} está mais barato que {price}$, é hora de comprar!"'

        return stock, msg, from_email

    def send(self):
        
        subject, msg, email = self.get_info()

        send_mail(
            subject=f'Ativo - {subject}',
            message=msg,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email]
        )