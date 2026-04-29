from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views import (
    login_view, logout_view, bulk_import, IncidentViewSet,
    forgot_password, verify_otp, reset_password,
)

router = DefaultRouter()
router.register(r'incidents', IncidentViewSet, basename='incident')

urlpatterns = [
    path('admin/',                  admin.site.urls),
    path('api/login/',              login_view),
    path('api/logout/',             logout_view),
    path('api/incidents/bulk/',     bulk_import),

    # ← Password reset BEFORE router
    path('api/forgot-password/',    forgot_password),
    path('api/verify-otp/',         verify_otp),
    path('api/reset-password/',     reset_password),

    # ← Router LAST (only once)
    path('api/',                    include(router.urls)),
]