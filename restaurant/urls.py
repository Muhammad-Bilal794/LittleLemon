from django.urls import path,include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'Booking/tables', views.BookingViewSet)

urlpatterns = [
    path('', views.index, name='index'),
    path('menu/', views.MenuItemsView.as_view()),
    path('menu/<int:pk>/', views.SingleMenuItemView.as_view()),
     path('', include(router.urls)),
]