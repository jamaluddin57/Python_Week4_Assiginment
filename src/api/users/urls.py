from django.urls import path
from .views import UserListView, UserDetailView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterView

urlpatterns = [
    path('auth/token/',TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/',TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/register/<str:user_type>/', RegisterView.as_view(), name='auth_register'),
    path('<str:user_type>/list', UserListView.as_view(), name='user-list'),
    path('<str:user_type>/<int:id>/', UserDetailView.as_view(), name='user-detail'),
]