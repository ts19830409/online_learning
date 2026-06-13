from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from lms.views import CourseViewSet, LessonListCreateView, LessonRetrieveUpdateDestroyView
from users.views import ProfileView
from users.views import PaymentListView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from users.views import SubscriptionView
from rest_framework.permissions import AllowAny
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from users.views import PaymentCreateView
from users.views import PaymentStatusView


router = DefaultRouter()
router.register(r'courses', CourseViewSet)

urlpatterns = [
	path('admin/', admin.site.urls),
	path('api/', include(router.urls)),
	path('api/profile/<int:pk>/', ProfileView.as_view(), name='profile'),
	path('api/lessons/', LessonListCreateView.as_view(), name='lesson-list-create'),
	path('api/lessons/<int:pk>/', LessonRetrieveUpdateDestroyView.as_view(), name='lesson-detail'),
]

urlpatterns += [
    path('api/payments/', PaymentListView.as_view(), name='payment-list'),
]

urlpatterns += [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

urlpatterns += [
    path('api/subscription/', SubscriptionView.as_view(), name='subscription'),
]

schema_view = get_schema_view(
    openapi.Info(
        title="LMS API",
        default_version='v1',
        description="API for online learning platform",
    ),
    public=True,
    permission_classes=[AllowAny],
)

urlpatterns += [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

urlpatterns += [
    path('api/payment/create/', PaymentCreateView.as_view(), name='payment-create'),
]

urlpatterns += [
    path('api/payment/<int:payment_id>/status/', PaymentStatusView.as_view(), name='payment-status'),
]