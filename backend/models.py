from django.db import models

# Create your models here.
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone
from datetime import timedelta
from django.utils.timezone import make_aware
class CustomDateTimeField(models.DateTimeField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('default', timezone.now().replace(microsecond=0))
        super().__init__(*args, **kwargs)

class MyAccountManager(BaseUserManager):
    def create_user(self,name,email,password=None,**kwargs):
        if not email:
            raise ValueError("User must have an email")
        
        email = self.normalize_email(email)
        user = self.model(email=email,name=name,**kwargs)
        
        user.set_password(password)
        user.save()
        
        return user
    def create_superuser(self ,name, email, password,**kwargs):
        user = self.create_user(
            email = email,
            name  = name,
            password = password,
            **kwargs
        )

        user.is_admin = True
        user.is_staff = True 
        user.is_active = True
        user.is_verified = True
        user.is_superuser = True
        user.save(using=self._db)
        return 
    

class UserAccount(AbstractBaseUser):
    name = models.CharField(max_length=50, blank=False)
    email = models.EmailField(max_length=100, unique=True, blank=False)
    phone = models.CharField(max_length=20,blank=True, null=True)
    country = models.CharField(max_length=50,blank=True, null=True)
    image = models.CharField(max_length=250, blank=True,null=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = CustomDateTimeField()
    is_pending = models.BooleanField(default=False)
    is_submit = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_block = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name','image']
    objects = MyAccountManager()
    def __str__(self):
        return f"{self.name} - {self.email}"
    def has_perm(self, perm, obj=None):
        return self.is_admin
    def has_module_perms(self, app_label):
        return True


class Catogery(models.Model):
     name = models.CharField(max_length=50, blank=False)
     description=models.CharField(max_length=50, blank=False)


class Courses(models.Model):
       c_name = models.CharField(max_length=50, blank=False)
       catogery=models.ForeignKey(Catogery,on_delete=models.CASCADE,null=True)
       

class Video(models.Model):
    video = models.CharField(max_length=250, blank=True,null=True)
    name=models.CharField(max_length=250, blank=True,null=True)
    description=models.CharField(max_length=250, blank=True,null=True)
     

class Trainers(models.Model):
    course=models.ForeignKey(Courses,on_delete=models.CASCADE,null=True)
    name = models.CharField(max_length=50, blank=False)
    image=models.CharField(max_length=250, blank=True,null=True)
    experience=models.CharField(max_length=250, blank=True,null=True)
    email = models.EmailField(max_length=100, unique=True, blank=False)
    phone = models.CharField(max_length=20,blank=True, null=True)
    password=models.CharField(max_length=10,blank=False)
    certificate= models.CharField(max_length=250, blank=True,null=True)
    is_blocked=models.BooleanField(default=False)
    is_approved=models.BooleanField(default=False)
    video_approval=models.BooleanField(default=False)
    course_fee=models.CharField(max_length=10,null=True)
    t_video=models.ForeignKey(Video,on_delete=models.CASCADE,null=True,related_name='trainers_videos')
    def __str__(self):
        return self.name     
    


class Subscription(models.Model):
        user=models.ForeignKey(UserAccount,models.CASCADE,null=True)
        trainer=models.ForeignKey(Trainers,models.CASCADE,null=True)
        payment_method=models.CharField(max_length=100,null=True)
        date=models.DateField(null=True)
        amount=models.PositiveIntegerField(null=True)

class Appointment(models.Model):
    trainer = models.ForeignKey(Trainers, on_delete=models.CASCADE)
    time = models.TimeField(null=True)
    date=models.DateField(null=True)
    

class Booking(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    is_booked=models.BooleanField(default=False)



class TrainerReview(models.Model):
    t_trainer = models.ForeignKey(Trainers, on_delete=models.CASCADE,null=True)
    t_user = models.ForeignKey(UserAccount, on_delete=models.CASCADE,null=True)
    rating = models.PositiveIntegerField(null=True)  
    review_text = models.TextField(null=True)