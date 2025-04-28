from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User
from .serializers import UserRegSerializer, ProfileSerializer
from rest_framework import status
from rest_framework import permissions
from django.core.mail import send_mail
from django.http import HttpResponse
from django.conf import settings
import requests
from decouple import config
from rest_framework_simplejwt.tokens import RefreshToken

# Create your views here.


BREVO_API_KEY = config("BREVO_API_KEY")
SENDER_EMAIL = config("SENDER_EMAIL")


def send_otp_email(to_email, subject, body):
    """
    Sends an email using the Brevo (Sendinblue) API.
    """
    url = "https://api.brevo.com/v3/smtp/email"
    headers = {
        "api-key": BREVO_API_KEY,
        "Content-Type": "application/json"
    }
    data = {
         "sender": {
            "name": "CareerMatterNG",  # Updated to CareerMatterNG
            "email": SENDER_EMAIL  # Must be a verified email in Brevo
        },
        "to": [{"email": to_email}],
        "subject": subject,
        "textContent": body
    }

    try:
        response = requests.post(url, headers=headers, json=data, timeout=10)  # Added timeout
        response.raise_for_status()  # Raises an error for HTTP 4xx or 5xx
        return response
    except requests.exceptions.Timeout:
        print("❌ ERROR: Connection to Brevo API timed out.")
        return None
    except requests.exceptions.RequestException as e:
        print(f"❌ ERROR: {e}")
        return None









class RegisterUserView(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer=UserRegSerializer(users, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    
    
    def post(self, request):
        serializer = UserRegSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.validated_data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class UserDetailView(APIView):

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            return None

    def get(self, request, pk):
        user = self.get_object(pk)
        if user is None:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserRegSerializer(user)
        return Response(serializer.data)

    def put(self, request, pk):
        user = self.get_object(pk)
        if user is None:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserRegSerializer(user, data=request.data, partial=True)  # partial=True for PATCH-like update
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user = self.get_object(pk)
        if user is None:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        user.delete()
        return Response({"message": "User deleted successfully."}, status=status.HTTP_204_NO_CONTENT)



class ProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = ProfileSerializer(request.user.profile)
        return Response(serializer.data)

    def put(self, request):
        serializer = ProfileSerializer(request.user.profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh_token")
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({"message": "Logout successful"}, status=status.HTTP_205_RESET_CONTENT)

        except Exception as e:
            return Response({"error": "Invalid refresh token"}, status=status.HTTP_400_BAD_REQUEST)





def test_email(request):
    send_otp_email(
        to_email="techbro0013@gmail.com",
        subject="Test from Brevo API",
        body="This is a test email sent using the Brevo API!"
    )
    # return HttpResponse("Test email sent!")