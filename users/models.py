from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
	def create_user(self, email, password=None, **extra_fields):
		if not email:
			raise ValueError('Email обязателен')
		email = self.normalize_email(email)
		user = self.model(email=email, **extra_fields)
		user.set_password(password)
		user.save()
		return user
	
	def create_superuser(self, email, password=None, **extra_fields):
		extra_fields.setdefault('is_staff', True)
		extra_fields.setdefault('is_superuser', True)
		return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
	username = None
	email = models.EmailField(unique=True, verbose_name='Email')
	phone = models.CharField(max_length=35, blank=True, null=True, verbose_name='Телефон')
	city = models.CharField(max_length=100, blank=True, null=True, verbose_name='Город')
	avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name='Аватар')
	
	objects = UserManager()
	
	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = []
	
	class Meta:
		verbose_name = 'Пользователь'
		verbose_name_plural = 'Пользователи'
	
	def __str__(self):
		return self.email


class Payment(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments', verbose_name='Пользователь')
	payment_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата оплаты')
	course = models.ForeignKey('lms.Course', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Курс')
	lesson = models.ForeignKey('lms.Lesson', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Урок')
	amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Сумма оплаты')
	payment_method = models.CharField(max_length=20, choices=[('cash', 'Наличные'), ('transfer', 'Перевод на счет')],
	                                  verbose_name='Способ оплаты')
	stripe_session_id = models.CharField(max_length=255, blank=True, null=True, verbose_name='ID сессии Stripe')
	stripe_product_id = models.CharField(max_length=255, blank=True, null=True, verbose_name='ID продукта Stripe')
	stripe_price_id = models.CharField(max_length=255, blank=True, null=True, verbose_name='ID цены Stripe')
	payment_url = models.URLField(blank=True, null=True, verbose_name='Ссылка на оплату')
	status = models.CharField(max_length=20, default='pending', verbose_name='Статус платежа')
	
	class Meta:
		verbose_name = 'Платёж'
		verbose_name_plural = 'Платежи'
	
	def __str__(self):
		return f'{self.user.email} - {self.amount} руб.'


class Subscription(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions')
	course = models.ForeignKey('lms.Course', on_delete=models.CASCADE, related_name='subscriptions')
	
	class Meta:
		unique_together = ['user', 'course']
		verbose_name = 'Подписка'
		verbose_name_plural = 'Подписки'
	
	def __str__(self):
		return f'{self.user.email} - {self.course.title}'