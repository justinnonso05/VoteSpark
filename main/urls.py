from django.urls import path, include
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from .views import (
    CreateElectionView, UpdateElectionView, ElectionListView, ElectionDetailView,
    AddPositionView, UpdatePositionView, PositionListView,
    AddCandidateView, UpdateCandidateView, CandidateListView, LoginView, SignupView
)

# Include router URLs in urlpatterns
urlpatterns = [
    path('auth/signup/', SignupView.as_view(), name='host_signup'),
    path('auth/login/', LoginView.as_view(), name='host_login'),
   # Elections
    path('election/all/', ElectionListView.as_view(), name='election-list'),
    path('election/create/', CreateElectionView.as_view(), name='election-create'),
    path('election/<int:pk>/', ElectionDetailView.as_view(), name='election-detail'),
    path('election/edit/<int:pk>/', UpdateElectionView.as_view(), name='election-update'),

    # Positions
    path('position/all/', PositionListView.as_view(), name='position-list'),
    path('position/add/', AddPositionView.as_view(), name='position-add'),
    path('position/<int:pk>/', UpdatePositionView.as_view(), name='position-update'),

    # Candidates
    path('candidate/all/', CandidateListView.as_view(), name='candidate-list'),
    path('candidate/add/', AddCandidateView.as_view(), name='candidate-add'),
    path('candidate/<int:pk>/', UpdateCandidateView.as_view(), name='candidate-update'),

    # Spectacular Schema & Swagger UI
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
]
