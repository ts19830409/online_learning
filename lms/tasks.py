from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from users.models import Subscription, User
from lms.models import Course
from django.utils import timezone


@shared_task
def send_course_update_email(course_id):
	"""Отправляет письма подписчикам при обновлении курса"""
	course = Course.objects.get(pk=course_id)
	if course.updated_at and (timezone.now() - course.updated_at).seconds < 4 * 3600:
		return
	
	subscribers = Subscription.objects.filter(course=course)
	emails = [sub.user.email for sub in subscribers]
	
	if emails:
		send_mail(
			subject=f'Курс "{course.title}" обновлён',
			message=f'Материалы курса "{course.title}" были обновлены. Зайдите в личный кабинет.',
			from_email=settings.DEFAULT_FROM_EMAIL,
			recipient_list=emails,
			fail_silently=False,
		)


@shared_task
def deactivate_inactive_users():
	"""Блокирует пользователей, не заходивших более 30 дней"""
	month_ago = timezone.now() - timezone.timedelta(days=30)
	users = User.objects.filter(last_login__lt=month_ago, is_active=True)
	count = users.update(is_active=False)
	return f'Deactivated {count} users'