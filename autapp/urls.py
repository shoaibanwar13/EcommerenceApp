
from django.urls import path
from autapp import views
urlpatterns = [
    path('signup/', views.signup,name="signup"),
    path('loginfunction/', views.loginfunction,name="loginfunction"),
    path('logoutfunction/', views.logoutfunction,name="logoutfunction"),
    path('activate/<uidb64>/<token>',views.ActtivateAccountView.as_view(),name="activate"),
    path('request-reset-email/',views.RequestResetEmailView.as_view(),name='request-reset-email'),
    path('set-new-password/<uidb64>/<token>',views.SetNewPasswordView.as_view(),name='set-new-password'),
   
]
