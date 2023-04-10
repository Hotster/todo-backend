from django.urls import path, include
from rest_framework import routers

from goals.views import GoalAPIView, FolderAPIView

router = routers.DefaultRouter()

router.register(r'goals', GoalAPIView, basename='goal')
router.register(r'folders', FolderAPIView, basename='folder')

urlpatterns = [
    path('', include(router.urls)),
]
