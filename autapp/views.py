from django.shortcuts import render,HttpResponse,redirect
#For Security Of sites 
from django.views.generic import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.urls import NoReverseMatch,reverse
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes,force_str,DjangoUnicodeDecodeError
from .utlis import generate_token
from django.contrib.auth.tokens import PasswordResetTokenGenerator
#For sendind Email
from django.core.mail import send_mail,EmailMultiAlternatives
from django.core.mail import BadHeaderError,send_mail
from django.core import mail
from django.core.mail import EmailMessage,EmailMultiAlternatives
from django.conf import settings
import threading
class EmailThread(threading.Thread):
    def __init__(self,email_message):
        self.email_message=email_message
        threading.Thread.__init__(self)
    def run(self):
        self.email_message.send()

def signup(request):
    if request.method=="POST":
        email=request.POST['email']
        password=request.POST['pass1']
        confirm_password=request.POST['pass2']
        username=email
        if password !=confirm_password:
            messages.warning(request,"Password does not match")
            return redirect('/autapp/signup/')
        try:
            
          if User.objects.get(username=email):
              messages.warning(request,"Email already taken")
              return redirect('/autapp/signup/')
          
        except Exception as identifier:
            pass
        user=User.objects.create_user(email,email,password)
        user.is_active=False
        current_site=get_current_site(request)
        user.save()
        
        email_subject="Activate Your Account"
        message=render_to_string('activate.html',{
            'user':user,
            'domain':'http://127.0.0.1:8000',
            'uid':urlsafe_base64_encode(force_bytes(user.pk)),
            'token':generate_token.make_token(user)
        })
        email_message=EmailMultiAlternatives(email_subject,message,settings.EMAIL_HOST_USER,[email])
        email_message.attach_alternative(email_subject,"text/html")
        EmailThread(email_message).start()
        messages.info(request,"Email have ben set to you email please click the link and activate account")
        return redirect('/autapp/loginfunction/')
        
        
    return render(request,"signup.html")

           
    

def loginfunction(request):
      if request.method == 'POST':
        # get parameters
        loginusername=request.POST['email']
        loginpassword=request.POST['pass1']
        user=authenticate(username=loginusername,password=loginpassword)
       
        if user is not None:
            login(request,user)
            messages.info(request,"Successfully Logged In")
            return render(request,"base.html")

        else:
            messages.error(request,"Invalid Credentials")
            return redirect('/autapp/loginfunction/')    
      return render(request,"login.html")
def logoutfunction(request):
    logout(request)
    messages.success(request,"Logout Successfully")
    return redirect('/autapp/loginfunction/')   
class ActtivateAccountView(View):
     def get(self,request,uidb64,token):
         
            try:
                
                uid=force_str(urlsafe_base64_decode(uidb64))
                user=User.objects.get(pk=uid)
            except Exception as identifier:
                 user=None
            if user is not None and generate_token.check_token(user,token):
                
               user.is_active=True
               user.save()
               messages.info(request,"Account Activated Successfully")
            return redirect('/autapp/loginfunction/')
            return render(request,'activatefail.html')
    
class RequestResetEmailView(View):
    def get(self,request):
        return render(request,'request-reset-email.html')
    
    def post(self,request):
        email=request.POST['email']
        user=User.objects.filter(email=email)

        if user.exists():
            current_site=get_current_site(request)
            email_subject='[Reset Your Password]'
            message=render_to_string('reset-user-password.html',{
                'domain':'127.0.0.1:8000',
                'uid':urlsafe_base64_encode(force_bytes(user[0].pk)),
                'token':PasswordResetTokenGenerator().make_token(user[0])
            })

            email_message=EmailMessage(email_subject,message,settings.EMAIL_HOST_USER,[email])
            email_message.send()

            messages.info(request,f"WE HAVE SENT YOU AN EMAIL WITH INSTRUCTIONS ON HOW TO RESET THE PASSWORD {message} " )
            return render(request,'request-reset-email.html')

class SetNewPasswordView(View):
    def get(self,request,uidb64,token):
        context = {
            'uidb64':uidb64,
            'token':token
        }
        try:
            user_id=force_str(urlsafe_base64_decode(uidb64))
            user=User.objects.get(pk=user_id)

            if  not PasswordResetTokenGenerator().check_token(user,token):
                messages.warning(request,"Password Reset Link is Invalid")
                return render(request,'request-reset-email.html')

        except DjangoUnicodeDecodeError as identifier:
            pass

        return render(request,'set-new-password.html',context)

    def post(self,request,uidb64,token):
        context={
            'uidb64':uidb64,
            'token':token
        }
        password=request.POST['pass1']
        confirm_password=request.POST['pass2']
        if password!=confirm_password:
            messages.warning(request,"Password is Not Matching")
            return render(request,'set-new-password.html',context)
        
        try:
            user_id=force_str(urlsafe_base64_decode(uidb64))
            user=User.objects.get(pk=user_id)
            user.set_password(password)
            user.save()
            messages.success(request,"Password Reset Success Please Login with NewPassword")
            return redirect('/autapp/loginfunction/')

        except DjangoUnicodeDecodeError as identifier:
            messages.error(request,"Something Went Wrong")
            return render(request,'set-new-password.html',context)


# Create your views here.
