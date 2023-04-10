from rest_framework.viewsets import ModelViewSet

from goals.models import Goal, Folder
from goals.serializers import GoalSerializer, FolderSerializer


class GoalAPIView(ModelViewSet):
    serializer_class = GoalSerializer

    def get_queryset(self):
        queryset = Goal.objects.filter(owner=self.request.user).order_by("-creation_date")
        return queryset


class FolderAPIView(ModelViewSet):
    serializer_class = FolderSerializer

    def get_queryset(self):
        queryset = Folder.objects.filter(owner=self.request.user).order_by("name")
        return queryset
