from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    
    path('trainerstatuschange',TrainerChangeStatus.as_view(), name='login_view'),
    
    path('alluser',Allusers.as_view(), name='login_view'),
      path('signup/', SignupView.as_view(), name='signup_view'),
      path('login/', LoginViews.as_view(), name='login_view'),
      path('logins/', LoginViews.as_view(), name='login_view'),
      path('adminlogin/', AdminLogin.as_view(), name='login_view'),
      path('blockuser/', Adminblockuser.as_view(), name='login_view'),
      path('unblockuser/', Adminunblockuser.as_view(), name='login_view'),
      path('blocktrainer/', Adminblocktrainer.as_view(), name='login_view'),
      path('unblocktrainer/', Adminunblocktrainer.as_view(), name='login_view'),
      path('uploadimage/', UploadImage.as_view(), name='login_view'),
      path('trainersignup/', TrainerSignup.as_view(), name='login_view'),
      path('trainerapproval/', Trainerapproval.as_view(), name='login_view'),
       path('trainercertificate/', TrianerCertificateVerification.as_view(), name='login_view'),
path('trainerlogin/', TrainerLogin.as_view(), name='login_view'),
path('addcato/', AddCatogery.as_view(), name='login_view'),
path('addcourse/', AddCourse.as_view(), name='login_view'),
path('uploadvideo/', TrainerVideoUpload.as_view(), name='login_view'),
path('videos/', TrainerVideos.as_view(), name='login_view'),
path('usercatoview/', SpacifiCato.as_view(), name='login_view'),
path('trinerview/',ViewTrainer.as_view(), name='login_view'),
path('trainerimage/',TrainerImage.as_view(), name='login_view'),
path('trainerfulldetails/',TrainerFullDetails.as_view(), name='login_view'),
path('admincoursefull/',AdminCourseFull.as_view(), name='login_view'),
path('trainervideosfull/',AdminVideos.as_view(), name='login_view'),
path('mail/',OtpVerification.as_view(), name='login_view'),
path('suscription/',Subscriptions.as_view(), name='login_view'),
path('sdetails/',SubscribedDetials.as_view(), name='login_view'),
path('usertrainersub/',UserTrainerSubscribers.as_view(), name='login_view'),
path('slot/',Slot.as_view(), name='login_view'),
path('myslots/',MySlots.as_view(), name='login_view'),
path('userslotview/',UserSlotView.as_view(), name='login_view'),
path('bookingslots/',BookingSlot.as_view(), name='login_view'),
path('mybookinstatus/',UserBookingStatusView.as_view(), name='login_view'),
path('myuserstatus/',MyUsersStatus.as_view(), name='login_view'),
path('updates/',ChangeStatusofUser.as_view(), name='updates'),
path('adminappoint/',AdminAppointmentview.as_view(), name='updates'),
path('adminbooking/',AdminBookingStatusView.as_view(), name='updates'),
path('mysubscribers/',MySubscribers.as_view(), name='updates'),
path('admindashboard/',DashBoard.as_view(), name='updates'),
path('review/',TrainerReviews.as_view(), name='updates'),
path('getreview/',ReviewDetails.as_view(), name='updates'),
path('allcato/',Allcatogery.as_view(), name='updates'),
path('allcour/',AllCourse.as_view(), name='updates'),
path('alltrainers/',AllTrainers.as_view(), name='updates'),
path('earnings/',Earnings.as_view(), name='updates'),
path('myvideos/',Myvideos.as_view(), name='updates'),
path('videochatlink/',VideoChatLink.as_view(), name='updates'),


]


