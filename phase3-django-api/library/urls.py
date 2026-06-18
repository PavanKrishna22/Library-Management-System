from .views import *
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r"libraries", LibraryViewSet)
router.register(r"authors", AuthorViewSet)
router.register(r"categories", CategoryViewSet)
router.register(r"books", BookViewSet)
router.register(r"members", MemberViewSet)
router.register(r"borrowings", BorrowingViewSet)
router.register(r"reviews", ReviewViewSet)

urlpatterns = [
    path("", health_check),
    path("statistics/", statistics),
    path("", include(router.urls)),

]