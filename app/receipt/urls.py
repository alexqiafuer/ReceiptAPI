"""
URL mappings for receipt
"""

from django.urls import path, include

from rest_framework.routers import DefaultRouter

from receipt import views

router = DefaultRouter()
router.register('receipts', views.ReceiptViewSet)
router.register('items', views.ItemViewSet)

app_name = 'receipt'

urlpatterns = [
    path('', include(router.urls)),
]
