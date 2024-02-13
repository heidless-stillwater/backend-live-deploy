from rest_framework.generics import ListAPIView
from rest_framework import permissions

from .models import Research
from .serializers import ResearchSerializer


class ResearchListView(ListAPIView):
    permission_classes = (permissions.AllowAny, )
    queryset = Research.objects.all()
    serializer_class = ResearchSerializer
    pagination_class = None