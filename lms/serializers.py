from rest_framework import serializers
from lms.models import Course, Lesson
from lms.validators import validate_youtube_link

class LessonSerializer(serializers.ModelSerializer):
	
	video_link = serializers.URLField(validators=[validate_youtube_link])
	
	class Meta:
		model = Lesson
		fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
	lessons_count = serializers.SerializerMethodField()
	lessons = LessonSerializer(many=True, read_only=True)
	
	class Meta:
		model = Course
		fields = '__all__'
	
	def get_lessons_count(self, obj):
		return obj.lessons.count()