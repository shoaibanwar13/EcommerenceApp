from django.shortcuts import render,redirect,HttpResponse
from .models import *
from math import ceil
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from Wooapp.utlis import render_to_pdf
from django.core.mail import send_mail,EmailMultiAlternatives
from django.core.mail import BadHeaderError,send_mail
from django.core import mail
from django.core.mail import EmailMessage
from django.conf import settings
import datetime
def index(request):
    
    allProds = []
    catprods = Product.objects.values('category','id')
    print(catprods)
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod= Product.objects.filter(category=cat)
        n=len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])

    params= {'allProds':allProds}
    

    return render(request,"index.html",params) 
def contact(request):
    if request.method=="POST":
        name=request.POST['name']
        email=request.POST['email']
        desc=request.POST['desc']
        phone=request.POST['pnumber']
        myuser=Contact(name=name,emai=email,desc=desc,phone=phone)
        myuser.save()
        messages.info(request,"we will get back to you soon..")
    return render(request,"contact.html")
def aboutus(request):
    return render(request,"About.html")
def service(request):
    service_data=Service.objects.all()
    data={
        'service_data':service_data
    }
    return render(request,"service.html",data)
    
def emailsub(request):
    if request.method=="POST":
        email=request.POST['email']
        subcription=emailsubcription(email=email)
        subcription.save()
        messages.success(request,"Thank you for Subscribe")
    return render(request,"index.html")
def returnproduct(request):
    if not request.user.is_authenticated:
        messages.warning(request,"Login and Try Again")
        return redirect('/autapp/loginfunction/')
    if request.method=="POST":
        name=request.POST['name']
        email=request.POST['email']
        pname=request.POST['pname']
        pid=request.POST['pid']
        reason=request.POST['reason']
        address=request.POST['address']
        zip=request.POST['zip']
        city=request.POST['city']
        state=request.POST['state']
        pnumber=request.POST['pnumber']
        data={
         'today':datetime.date.today(), 
          'name':name,
          'email':email,
          'pname':pname,
          'pid':pid,
          'reason':reason,
          'address':address,
          'zip':zip,
          'city':city,
          'state':state,
          'pnumber':pnumber
        }
        #pdf = render_to_pdf('invoice.html', data)
        #email_subject=['Product Return Invoice']
        #message=pdf
        #email_message=EmailMessage(email_subject,message,settings.EMAIL_HOST_USER,[email])
        #email_message.send()
        returp=ReturnProduct(name=name,email=email,pname=pname,pid=pid,reason=reason,address=address,zip=zip,city=city,state=state,pnumber=pnumber)
        returp.save()
        messages.success(request,"Your information about return product have been recevied and a conformation Email have set to your email message")
        
    return render(request,"return-product.html")
def checkout(request):
    return render(request,"checkout.html")
def returnhistory(request):
    if not request.user.is_authenticated:
        messages.warning(request,"Login and Try Again")
        return redirect('/autapp/loginfunction/')
        
    currentuser=request.user.username
    status=ReturnProduct.objects.filter(email=currentuser)
    getstatus={
        'status':status
    }
    getdata=ReturnProduct.objects.all()
    context={
            'getdata':getdata
        }
    return render(request,"returnhistory.html",context,getstatus)
# Create your views here.
