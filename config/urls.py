from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from lms.views import CourseViewSet, LessonListCreateView, LessonRetrieveUpdateDestroyView
from users.views import ProfileView
from users.views import PaymentListView

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