from django.urls import path, include
from rest_framework.routers import DefaultRouter

from quote import views

router = DefaultRouter()
router.register('quote', views.QuoteViewSet)

app_name = 'quote'

urlpatterns = [
    path('', include(router.urls)),
]
