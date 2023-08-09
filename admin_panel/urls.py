from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from admin_panel.views import LoginView, LogoutView, ChangePasswordView, MainPageDataView

urlpatterns = [
    path('accounts/login', LoginView.as_view(), name='register'),
    path('accounts/logout', LogoutView.as_view(), name='register'),
    path('accounts/change-password', ChangePasswordView.as_view(), name='register'),
    path('accounts/token-refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('main-page-data/', MainPageDataView.as_view(), name='main_page_data'),
]
