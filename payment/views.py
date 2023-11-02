from django.shortcuts import render
from .models import Product
from .payment import Payload


def index(request):
    products = Product.objects.all()
    return render(request, "payment/pages/index.html",{
        "products": products,
    })
    
def product_page(request, id):
    product = Product.objects.get(id=id)
    return render(request, "payment/pages/product_payment_page.html",{
        "product": product,
    })
    
def pix(request, id):
    product = Product.objects.get(id=id)
    formatted_price = "{:.2f}".format(product.price)
    txtId = str(product.name).strip()[:40] 
    txtId = ''.join(e for e in txtId if e.isalnum() or e in (' ', '-', '_'))  
    
    pix_payload = Payload('Ciborg Inc.', 'matheusricardo164@gmail.com', formatted_price, 'Manacapuru', txtId)
    qrcode_base64 = pix_payload.gerarPayload()
    pix_copy_paste = pix_payload.gerarPayloadString()
 
    return render(request, "payment/pages/pix_page.html",{
        "product": product,
        'pix_copy_paste': pix_copy_paste,
        'qrcode_base64': qrcode_base64,
    })


