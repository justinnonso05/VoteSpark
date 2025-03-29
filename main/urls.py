from django.urls import path, include
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from .views import (
    ElectionView, PositionView,
    CandidateView, VoterView, LoginView, SignupView
)

# Include router URLs in urlpatterns
urlpatterns = [
    path('auth/signup/', SignupView.as_view(), name='host_signup'),
    path('auth/login/', LoginView.as_view(), name='host_login'),
    path('api/election/', ElectionView.as_view(), name='election'),
    path('api/candidate/', CandidateView.as_view(), name='candidate'),

    # Spectacular Schema & Swagger UI
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
]
