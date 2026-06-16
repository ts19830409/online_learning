from django.db import models
from django.conf import settings

class Course(models.Model):
	title = models.CharField(max_length=200, verbose_name='Название')
	preview = models.ImageField(upload_to='courses/', blank=True, null=True, verbose_name='Превью')
	description = models.TextField(verbose_name='Описание')
	owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True,
	                          verbose_name='Владелец')
	price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Цена')
	updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
	
	class Meta:
		verbose_name = 'Курс'
		verbose_name_plural = 'Курсы'
	
	def __str__(self):
		return self.title


class Lesson(models.Model):
	title = models.CharField(max_length=200, verbose_name='Название')
	description = models.TextField(verbose_name='Описание')
	preview = models.ImageField(upload_to='lessons/', blank=True, null=True, verbose_name='Превью')
	video_link = models.URLField(verbose_name='Ссылка на видео')
	course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons', verbose_name='Курс')
	owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True,
	                          verbose_name='Владелец')
	
	class Meta:
		verbose_name = 'Урок'
		verbose_name_plural = 'Уроки'
	
	def __str__(self):
		return self.title