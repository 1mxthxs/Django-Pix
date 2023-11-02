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
    
    print(product.name) 
    txtId = str(product.name).strip()[:40]  # Truncate to 40 characters or the max length allowed for txtId
    print(txtId)  
    txtId = ''.join(e for e in txtId if e.isalnum() or e in (' ', '-', '_'))  # Removendo caracteres especiais

    pix_copy_paste = Payload('Ciborg Inc.', 'matheusricardo164@gmail.com', formatted_price, 'Manacapuru', txtId).gerarPayload()
 
    
    
    print(txtId)  
    #pix_copy_paste = Payload('Cibog Inc.', 'matheusricardo164@gmail.com', formatted_price, 'Manacapuru', 'Ciborg').gerarPayload()

    
    return render(request, "payment/pages/pix_page.html",{
        "product": product,
        'pix_copy_paste': pix_copy_paste,
    })


