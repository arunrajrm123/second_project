
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import *

import hashlib
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions
from rest_framework.validators import ValidationError
from django.contrib.auth import authenticate


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    def validate(self, data):
        print(data)
        email = data.get("email")
        password = data.get("password")
        if email and password:
            user = authenticate(email=email, password=password)
            if user:
                if not user.is_active:
                    raise serializers.ValidationError(
                        "You are not authorized to perform this action"
                    )
                else:
                    data["user"] = user
            else:
                raise serializers.ValidationError("Invalid username or password")
        else:
            raise serializers.ValidationError("Email and Password are required")
        return data



class UserAccountSerializer(ModelSerializer):
    class Meta:
        model=UserAccount
        fields= "__all__"


class TrainerSerializer(ModelSerializer):
    class Meta:
        model=Trainers
        fields="__all__"


class CatogerySerailizer(ModelSerializer):
    class Meta:
        model=Catogery
        fields="__all__"

class CourseSerailzer(ModelSerializer):
    class Meta:
        model=Courses
        fields="__all__"


class VideoSerailzer(ModelSerializer):
    class Meta:
        model=Video
        fields="__all__"
class Subscriptionseri(serializers.ModelSerializer):
    trainer_details = serializers.SerializerMethodField()
    videos = serializers.SerializerMethodField()
    course=serializers.SerializerMethodField()
    user=serializers.SerializerMethodField()
    class Meta:
        model = Subscription
        fields = "__all__"
    def __init__(self, *args, **kwargs):
       
        self.user_id = kwargs.pop('user_id', None)
        super(Subscriptionseri, self).__init__(*args, **kwargs)
    def get_user(self,obj):
        users=obj.user
        return{
            "user_name":users.name,
            "user_email":users.email
        }
    def get_trainer_details(self, obj):
        trainer = obj.trainer
        return {
            'trainer_id': trainer.id,
            'trainer_name': trainer.name,
            'trainer_experience': trainer.experience,
            'trainer_image': trainer.image,
           
        }

    def get_videos(self, obj):
       
        videos = Video.objects.filter(id=obj.trainer.t_video.id)
        video_data = [] 
        for video in videos:
            video_data.append({
                'video': video.video,
                "video_name":video.name,
                'video_description': video.description,
              
            })
        return video_data
    def get_course(self,obj):
        course=Courses.objects.get(id=obj.trainer.course.id)
        return {
            "course_name":course.c_name
        }
class AppoitmentSeri(ModelSerializer):
    trainer_data = TrainerSerializer(source='trainer', read_only=False)

    class Meta:
        model=Appointment
        fields = "__all__"

class BookingSeri(ModelSerializer):
    user_data = UserAccountSerializer(source='user', read_only=True)
    appointment = serializers.SerializerMethodField()
    trainer = serializers.SerializerMethodField()

    class Meta:
        model = Booking
        fields = "__all__"

    def get_appointment(self, obj):
        appointment = obj.appointment
        return {
            "appointment_time": appointment.time.strftime('%H:%M:%S'),
            "appointment_date": appointment.date.strftime('%Y-%m-%d'),
        }

    def get_trainer(self, obj):
        trainer = obj.appointment.trainer
        return {
            "trainer_name": trainer.name
        }


class TrainerReviewSeri(ModelSerializer):
    trainer_data = TrainerSerializer(source='t_trainer', read_only=False)
    user_data=UserAccountSerializer(source='t_user', read_only=False)
    user = serializers.SerializerMethodField()

    class Meta:
        model=TrainerReview
        fields = "__all__"

    def get_user(self,obj):
        users=obj.t_user.name
        return{
            "name":users
        }
        