
from django.urls import path
from Wooapp import views
urlpatterns = [
    path('', views.index,name="index"),
    path('contact/', views.contact,name="contact"),
    path('aboutus/', views.aboutus,name="aboutus"),
    path('service/', views.service,name="service"),
    path('emailsub/', views.emailsub,name="emailsub"),
    path('returnproduct/', views.returnproduct,name="returnproduct"),
    path('checkout/', views.checkout,name="checkout"),
    path('returnhistory/', views.returnhistory,name="returnhistory")
]
