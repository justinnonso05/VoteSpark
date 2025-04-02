from django.urls import path, include
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from .views import (
    CreateElectionView, CreatePositionView,
    CreateCandidateView, VoterView, LoginView, SignupView, ListPositionView
)

# Include router URLs in urlpatterns
urlpatterns = [
    path('auth/signup/', SignupView.as_view(), name='host_signup'),
    path('auth/login/', LoginView.as_view(), name='host_login'),
    path('api/election/create', CreateElectionView.as_view(), name='create-election'),
    path('api/candidate/create', CreateCandidateView.as_view(), name='create-candidate'),
    path('api/position/create', CreatePositionView.as_view(), name='create-position'),
    path('api/position/list', ListPositionView.as_view(), name='list-position'),

    # Spectacular Schema & Swagger UI
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
]
