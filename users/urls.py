from django.urls import path
from .views import RegisterUserView, ProfileView , test_email, UserDetailView, LogoutView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView



urlpatterns = [
    path('register/', RegisterUserView.as_view(), name="register"),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', ProfileView.as_view(), name='profile-view'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('test-email/', test_email),
    



]

