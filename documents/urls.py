from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views
from .views import LoginViewSet, DocumentViewSet , ProtectedCheckView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'documents', DocumentViewSet)

urlpatterns = [
    path('auth/login/', LoginViewSet.as_view(), name='login'),  # Login endpoint
    path('protected-check/', ProtectedCheckView.as_view()),# # Protected endpoint to check if token is valid

    path('auth/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),  # Refresh token endpoint
    path('', include(router.urls)),  # Document endpoints
]
