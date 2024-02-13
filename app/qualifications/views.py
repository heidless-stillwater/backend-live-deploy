from rest_framework.generics import ListAPIView
from rest_framework import permissions

from .models import Qualifications
from .serializers import QualificationsSerializer


class QualificationsListView(ListAPIView):
    permission_classes = (permissions.AllowAny, )
    queryset = Qualifications.objects.all()
    serializer_class = QualificationsSerializer
    pagination_class = None