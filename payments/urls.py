from django.urls import path
from . import views

urlpatterns = [
	path('payment_page', views.payment_page, name='payment_page'),
	path('posttozaakpay', views.posttozaakpay, name='posttozaakpay'),
	path('response', views.response, name='response'),
]
