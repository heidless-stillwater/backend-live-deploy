from django.urls import path
from .views import ResearchListView

urlpatterns = [
    path('', ResearchListView.as_view()),
]