from django.urls import path
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from package.views import (
    PackageViewset,
    PackageDetailViewset
)


router = DefaultRouter()
router.register("packages", PackageViewset, basename="package")
router.register("packageDetail", PackageDetailViewset, basename="packageDetail")


urlpatterns = [
    path("", include(router.urls)),
]
