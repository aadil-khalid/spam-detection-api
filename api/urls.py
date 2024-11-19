from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('mark-spam/', views.MarkSpamView.as_view(), name='mark_spam'),
    path('search-by-name/', views.SearchByNameView.as_view(), name='search_by_name'),
    path('search-by-phone/', views.SearchByPhoneNumberView.as_view(), name='search_by_phone_number'),
]
