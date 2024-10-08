from django.shortcuts import render, redirect
import mercadopago
import uuid
from .models import Product
sdk = mercadopago.SDK("SUA-SECRET-KEY")


# Lembre-se de identificar os usuários por sua sessão, aceitar pagamentos somente se
# o usuário tiver um cadastro. Após feito o pagamento libearar os recursos para o usuário.
def home(request):
    product = Product.objects.all()
    return render(request, 'inicio.html', {'obj':product})

# A requisição aqui deve ser POST
def process_transaction(request):
    if request.method == 'POST':
        request_options = mercadopago.config.RequestOptions()
        unique_key = uuid.uuid4().int >> 64
        # Na documentação do mercado pago, pede para que usemos um valor único para cada requisição
        # ao gerar um pagamento, e recomenda que seja um uuid v4.
        request_options.custom_headers = {
            'x-idempotency-key': str(unique_key)
        }
        # Alguns parâmetros abaixo não são obrigatórios.
        payment_data = {
            "transaction_amount": 100,
            "description": "Título do produto",
            "payment_method_id": "pix",
            "payer": {
                "email": "teste@gmail.com",
                "first_name": "Test",
                "last_name": "User",
                "identification": { # este dicionário é opcional
                    "type": "CPF",
                    "number": "OPCIONAL"
                }
            }
        }
        # Precisaremos somente de 'point_of_interaction' e 'transaction_data', ali é onde fica o
        # qr_code para ler e copiar. Na documentação podemos ver todos os parâmetros exibidos.
        payment_response = sdk.payment().create(payment_data, request_options)
        payment = payment_response["response"].get('point_of_interaction', {}).get('transaction_data')
        request.session['payment'] = payment
        print(payment)
    return redirect('show_qr')


def show_qr_code(request):
    payment_copy = request.session.get('payment').get('qr_code')
    payment_read = request.session.get('payment').get('qr_code_base64')
    return render(request, 'show_qr_code.html', {'payment':payment_copy, 'payment_read':payment_read})


# Não é possível fazer pagamentos PIX em contas teste do mercado pago.
# Temos que pegar a SECRET-KEY de pordução, da nossa conta real.

# Você terá que criar um webhook pelo mercado pago, isso porque ele nós informa
# quando ocorre um pagamento em nosso sistema, e retorna os dados do pagante.

# https://www.mercadopago.com.br/developers/pt/reference/payments/_payments/post
# https://www.mercadopago.com.br/developers/pt/docs/checkout-api/integration-configuration/integrate-with-pix