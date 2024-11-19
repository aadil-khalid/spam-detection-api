from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q, Count
from .models import User, Contact
from .serializers import UserSerializer, ContactSerializer
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth import authenticate

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        return Response({'error': 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)

class MarkSpamView(APIView):
    athuentication_class = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        phone_number = request.data.get('phone_number')
        contact, created = Contact.objects.get_or_create(user=request.user, phone_number=phone_number)
        contact.is_spam = True
        contact.save()
        return Response({'message': 'Marked as spam'})

class SearchByNameView(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ContactSerializer

    def get_queryset(self):
        name = self.request.query_params.get('name', '')
        starts_with_queryset = Contact.objects.filter(name__startswith=name).annotate(spam_count=Count('id', filter=Q(is_spam=True)))
        contains_queryset = Contact.objects.filter(name__icontains=name).exclude(name__startswith=name).annotate(spam_count=Count('id', filter=Q(is_spam=True)))
        queryset = starts_with_queryset | contains_queryset
        return queryset.order_by('-spam_count')

class SearchByPhoneNumberView(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ContactSerializer

    def get_queryset(self):
        phone_number = self.request.query_params.get('phone_number', '')
        queryset = Contact.objects.filter(phone_number=phone_number).annotate(spam_count=Count('id', filter=Q(is_spam=True)))
        return queryset.order_by('-spam_count')