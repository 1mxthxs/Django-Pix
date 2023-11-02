from django.urls import path
from . import views

app_name = 'payment'

urlpatterns = [
    path("", views.index, name="index"),
    path("product/<int:id>/", views.product_page, name="product_page"),
    path("product/pix/<int:id>/", views.pix, name="pix"),
]
