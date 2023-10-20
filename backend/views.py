from django.shortcuts import render
from django.shortcuts import render
from django.views import View 
from django.http import JsonResponse
from rest_framework.response import Response 
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.generics import CreateAPIView
from .models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
import random
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
import logging
class SignupView(APIView):
    def post(self,request):
        name=request.data.get("name")
        email=request.data.get("email")
        password=request.data.get("password")
        phonenumber=request.data.get("phonenumber")
        print(request.data,"allDATAS###################")
        otp = str(random.randint(100000, 999999))  
        datas={"name":name,"email":email,"password":password,"phonenumber":phonenumber,"otp":otp}
        print(email,otp)
        send_mail(
            'OTP Verification',
            f'Your OTP is: {otp}',
            "settings.EMAIL_HOST_USER",  
            [email],
            fail_silently=False,
        )
        print(send_mail)
        return Response({'message': 'OTP sent successfully',"data":datas})
    

class Allusers(APIView):
    def post(self,request):
        m=request.data.get("values")
        print(m)
        if m is None:
           s=UserAccount.objects.all()
           ser=UserAccountSerializer(s,many=True)
           print(ser)
           return Response(ser.data)
        else:
             print("entered",m)
             s=UserAccount.objects.filter(name__startswith=m)
             ser=UserAccountSerializer(s,many=True)
             if s==[]:
                  s=UserAccount.objects.all()
                  ser=UserAccountSerializer(s,many=True)
                  print(ser)
                  return Response(ser.data)
             else:
               return Response(ser.data)
       
       
    
class OtpVerification(CreateAPIView):
    def create(self,request):
        try:
            name=request.data.get("name")
            email=request.data.get("email")
            password=request.data.get("password")
            phonenumber=request.data.get("phone")
            print(name,email,password,phonenumber)
            user=UserAccount.objects.create(name=name,email=email,password=password,phone=phonenumber)
            print(user,"user")
            return Response({"message":"otp verified successfully"})
        except Exception as e:
            return Response({"mess":"error"})


class LoginViews(APIView):
    def post(self, request):
        try:
            email = request.data.get('email')
            password = request.data.get('password')
            userobj = UserAccount.objects.get(email=email, password=password)
            print(userobj)
            if  userobj:
                if not userobj.is_block:
                    refresh = RefreshToken.for_user(userobj)
                    serialized = UserAccountSerializer(userobj)
                    allus=UserAccount.objects.all()
                    seri=UserAccountSerializer(allus,many=True)
                    return Response({'message': 'Login successful', 'access': str(refresh.access_token), 'refresh': str(refresh), "alldatas": serialized.data,"alluserdetails":seri.data})
                else:
                     return Response({'message': 'You are blocked by admin'})
            else:
                return Response({'message': 'Invalid password'})
        except ObjectDoesNotExist:
            return Response({'message': 'User does not exist'})
        except Exception as e:
            return Response({'message': 'An error occurred'})


class AdminLogin(APIView):
    def post(self,request):
        email=request.data.get("email")
        password=request.data.get("password")
        try:
            userobj=UserAccount.objects.get(email=email,is_superuser=True)
            if userobj.check_password(password):
                print(userobj,"HHHHHHHHHHHH")
                refresh = RefreshToken.for_user(userobj)
                serialized=UserAccountSerializer(userobj)
                # ALL USERS DATAS
                userobjs=UserAccount.objects.all()
                tarinerobjs=Trainers.objects.all()
                tarinerserial=TrainerSerializer(tarinerobjs,many=True)
                serializedusers=UserAccountSerializer(userobjs,many=True)
                return Response({'message': 'Login successful', 'access': str(refresh.access_token), 'refresh': str(refresh),"trainerdatas":tarinerserial.data,"alldatas":serialized.data,"userdatas":serializedusers.data}) 
        except:
            return Response({"msg":"User Not found"})


class Adminblockuser(APIView):
    def put(self,request):
        id=request.data.get("id")
        userobj=UserAccount.objects.get(id=id)
        if userobj:
            userobj.is_block=True
            userobj.save()
            allusers=UserAccount.objects.all()
            serializedusers=UserAccountSerializer(allusers,many=True)
            print(userobj,"blockeduser")
            return Response({'message': 'Blocked successfully', "userdatas":serializedusers.data}) 


class Adminunblockuser(APIView):
    def put(self,request):
        id=request.data.get("id")
        userobj=UserAccount.objects.get(id=id)
        if userobj:
            userobj.is_block=False
            userobj.save()
            allusers=UserAccount.objects.all()
            serializedusers=UserAccountSerializer(allusers,many=True)
            print(userobj,"unblockeduser")
            print(serializedusers,'haii')
            return Response({'message': 'unblocked successfully', "userdatas":serializedusers.data}) 


class UploadImage(APIView):
    def post(self,request):
        print("view reached")
        print(request.data.get("imageurl"))
        print(request.data.get("userid"))
        userobj=UserAccount.objects.get(id=request.data.get("userid"))
        print(userobj)
        img=request.data.get("imageurl")
        userobj.image=img
        userobj.save()
        userdatas=UserAccount.objects.get(id=request.data.get("userid"))
        ser=UserAccountSerializer(userdatas)
        return Response({"msg":"success","imageurl":request.data.get("imageurl"),"userdatas":ser.data})


class TrainerSignup(APIView):
    def post(self,request):
        name=request.data.get("name")
        email=request.data.get("email")
        password=request.data.get("password")
        phonenumber=request.data.get("phonenumber")
        certificate=request.data.get("certificate")
        experience=request.data.get("experience")
        course=request.data.get("course")
        fee=request.data.get("course_fee")
        print(course)
        cour=Courses.objects.get(c_name=course)
        c=Catogery.objects.get(name=cour.catogery.name)
        courseseri=CourseSerailzer(cour)
        catoseri=CatogerySerailizer(c)
        print(certificate)
        print(c)
        trainerobj= Trainers.objects.create(name=name,email=email,password=password,phone=phonenumber,certificate=certificate,course=cour,course_fee=fee,experience=experience)
        trainerserialized=TrainerSerializer(trainerobj)
        print(trainerserialized)
        return Response({"trainerseri":trainerserialized.data,"courde":courseseri.data,"catode":catoseri.data})


class Trainerapproval(APIView):
    def get(self, request):
        signed_trainers = Trainers.objects.all()
        serializer = TrainerSerializer(signed_trainers, many=True)
        # Serialize the data and return it as JSON in the response
        serialized_data = serializer.data
        print(serialized_data)
        return Response({"trainers": serialized_data})
    

class TrianerCertificateVerification(APIView):
    def put(self,request):
        id=request.data.get("id")
        userobj=Trainers.objects.get(id=id)
        if userobj:
            userobj.is_approved=True
            userobj.save()
            allusers=Trainers.objects.all()
            serializedusers=TrainerSerializer(allusers,many=True)
            print(userobj,"approved")
            print(serializedusers,'haii')
            return Response({'message': 'approved', "trainerdatas":serializedusers.data}) 


class TrainerLogin(APIView):
    def post(self,request):
        try:
            email = request.data.get('email')
            password = request.data.get('password')
            userobj = Trainers.objects.get(email=email, password=password)
            tarinercato=Catogery.objects.get(id=userobj.course.id)
            trainercou=Courses.objects.get(id=userobj.course.id)
            print(tarinercato)
            print(userobj)
            logging.debug(userobj)
            if  userobj:
                if not userobj.is_approved:
                    print(userobj.is_approved,"not")
                    return Response({'message': 'You are Not approved by admin'}) 
                else:
                    if not userobj.is_blocked:
                        logging.debug("yes im entered to the refresh token method")
                        refresh = RefreshToken.for_user(userobj)
                        print(refresh)
                        logging.debug(refresh)
                        serialized = TrainerSerializer(userobj)
                        allseri=Trainers.objects.all()
                        alltrain=TrainerSerializer(allseri,many=True)
                        trainercat=CatogerySerailizer(tarinercato)
                        traincor=CourseSerailzer(trainercou)
                        print(serialized)
                        print( trainercat)
                        return Response({'message': 'Login successful', 'access': str(refresh.access_token), 'refresh': str(refresh),"traincor":traincor.data,"trainerscato":trainercat.data, "alldatas": serialized.data,"alltrainer": alltrain.data})
                    else:
                        return Response({'message': 'You are blocked by admin'})
            else:
                return Response({'message': 'Invalid password'})
        except ObjectDoesNotExist:
            return Response({'message': 'User does not exist'})
        except Exception as e:
            print(f"Exception: {str(e)}")
            return Response({'message': "error occuered"})

                    
class Adminblocktrainer(APIView):
    # //retrive update view
    def put(self,request):
        id=request.data.get("id")
        userobj=Trainers.objects.get(id=id)
        if userobj:
            userobj.is_blocked=True
            userobj.save()
            allusers=Trainers.objects.all()
            serializedusers=TrainerSerializer(allusers,many=True)
            print(userobj,"blockeduser")
            return Response({'message': 'Blocked successfully', "userdatas":serializedusers.data}) 


class Adminunblocktrainer(APIView):
    def put(self,request):
        id=request.data.get("id")
        userobj=Trainers.objects.get(id=id)
        if userobj:
            userobj.is_block=False
            userobj.save()
            allusers=Trainers.objects.all()
            serializedusers=TrainerSerializer(allusers,many=True)
            print(userobj,"unblockeduser")
            print(serializedusers,'haii')
            return Response({'message': 'unblocked successfully', "userdatas":serializedusers.data}) 
        


class AddCatogery(APIView):
    def post(self,request):
        name=request.data.get("name")
        allcat=Catogery.objects.all()
        s=[i.name for i in allcat]
        if name in s:
            return Response({"message":"Same name exists"})
        else:
            description=request.data.get("description")
            cato=Catogery.objects.create(name=name,description=description)
            print(cato)
            serializer=CatogerySerailizer(cato)
            allcato=Catogery.objects.all()
            allseri=CatogerySerailizer(allcato,many=True)
            print(allseri)
            return Response({"catodata":allseri.data})


class AddCourse(APIView):
    def post(self,request):
        name=request.data.get("name")
        catogery_name=request.data.get("catogery")
        print(catogery_name)
        cato=Catogery.objects.get(name=catogery_name)
        if not cato:
             return Response({"message":"catogery doesnt match"})
        else:
            print(cato)
            c=Courses.objects.get(c_name=name,catogery=cato)
            if  c:
                 print("yes")
                 return Response({"message":"already exist"})
               
            else:
                course=Courses.objects.create(c_name=name,catogery=cato)
                print(course)
                allcourse=Courses.objects.all()
                catoseril=CatogerySerailizer(cato)
                allseril=CourseSerailzer(allcourse,many=True)
                print(allseril)
                return Response({"allcourse":allseril.data,"catoserail":catoseril.data})
    
        
class TrainerVideoUpload(APIView):
        # nexted serializers,serilizer method feild,to representation,all api views,perform create
        def post(self,request):
            id=request.data.get("id")
            print(id)
            videourl=request.data.get("video")
            name=request.data.get("name")
            description=request.data.get("description")
            video=Video.objects.create(name=name,video=videourl,description=description)
            trainer=Trainers.objects.get(id=id)
            print(trainer)
            trainer.t_video=video
            trainer.save()
            seri=TrainerSerializer(trainer)
            vid=trainer.t_video
            return Response({"message":"video uploaded successfully"})
       
class TrainerVideos(APIView):
    def post(self,request):
        id=request.data.get("id")
        print(id)
        trainer=Trainers.objects.get(id=id)
        video =Video.objects.filter(trainers_videos=trainer).first()
        if video:
            s=video.video
            print(video.video)
            videoseril=VideoSerailzer(video)
            print(videoseril.data)
            return Response({"vid":s})
        else:
            return Response({"message":"no videos"})

class Allcatogery(APIView):
    def post(self,request):
        value=request.data.get("value")
        if value is None:
           c=Catogery.objects.all()
           seri=CatogerySerailizer(c,many=True)
           return Response(seri.data)
        else:
            c=Catogery.objects.filter(name__startswith=value)
            print(c)
            if c==[]:
                print("entered")
                c=Catogery.objects.all()
                seri=CatogerySerailizer(c,many=True)
                return Response(seri.data)
            else:
               seri=CatogerySerailizer(c,many=True)
               return Response(seri.data)
import re
from django.db.models import Q

class AllTrainers(APIView):
 def post(self,request):
    input_string=request.data.get("data")
    fee=request.data.get("fee")
    value=request.data.get("value")
    if  input_string is None:
        if value is None:
           c=Trainers.objects.all()
           seri=TrainerSerializer(c,many=True)
           return Response(seri.data)
        else:
            c=Trainers.objects.filter(name__startswith=value)
            print(c)
            if c==[]:
                print("entered")
                c=Trainers.objects.all()
                seri=TrainerSerializer(c,many=True)  
                return Response(seri.data)
            else:
               seri=TrainerSerializer(c,many=True)  
               return Response(seri.data)
    else:
        print("enteredss")
        print(input_string)
        if input_string=="":
                c=Trainers.objects.all()
                seri=TrainerSerializer(c,many=True)  
                return Response(seri.data)
        else:
            experience_regex = r'experience([<>=]+)(\d+)years'
            fees_regex = r'fees([<>=]+)(\d+)'
            experience_match = re.search(experience_regex, input_string)
            fees_match = re.search(fees_regex, input_string)
            operator = experience_match.group(1)
            value = int(experience_match.group(2))
            fee=int(fees_match.group(2))
            if operator == "<=":
                print("haii")
                c = Trainers.objects.filter(
                    Q(experience__lte=value) & Q(course_fee__lte=fee)
                )
                seri=TrainerSerializer(c,many=True)
                return Response(seri.data)
            else:
                print('hello')
                c = Trainers.objects.filter(
                    Q(experience__gte=value) & Q(course_fee__lte=fee)
                )
                seri=TrainerSerializer(c,many=True)
                return Response(seri.data)
        
           
        
class AllCourse(APIView):
    def post(self,request):
        value=request.data.get("value")
        if value is None:
           c=Courses.objects.all()
           seri=CourseSerailzer(c,many=True)
           return Response(seri.data)
        else:
            c=Courses.objects.filter(c_name__icontains=value)
            print(c)
            if c==[]:
                print("entered")
                c=Courses.objects.all()
                seri=CourseSerailzer(c,many=True)
                return Response(seri.data)
            else:
               seri=CourseSerailzer(c,many=True)
               return Response(seri.data)


class SpacifiCato(APIView):
    def post(self,request):
        id=request.data.get("id")
        print(id)
        cato=Catogery.objects.get(id=id)
        cor=Courses.objects.filter(catogery=cato)
        c=Courses.objects.all()
        print("c",c)
        print("cor",cor)
        seri=CourseSerailzer(cor,many=True)
        print("seri",seri.data)
        return Response(seri.data)


class ViewTrainer(APIView):
    def post(self,request):
        id=request.data.get("id")
        course=Courses.objects.get(id=id)
        trainer=Trainers.objects.filter(course=course)
        print(trainer)
        seri=TrainerSerializer(trainer,many=True)
        return Response(seri.data)
    
class TrainerImage(APIView):
    def post(self,request):
        id=request.data.get("id")
        image=request.data.get("image")
        print(image)
        Trainer=Trainers.objects.get(id=id)
        Trainer.image=image
        Trainer.save()
        print(Trainer)
        Train=Trainers.objects.get(id=id)
        seri=TrainerSerializer(Train)
        print(Train.image)
        return Response(seri.data)


class TrainerFullDetails(APIView):
    def post(self,request):
        id=request.data.get("id")
        Trainer=Trainers.objects.get(id=id)
        Trainser=TrainerSerializer(Trainer)
        return Response(Trainser.data)
    
class AdminCourseFull(APIView):
    def post(self,request):
        id=request.data.get("id")
        Ca=Catogery.objects.get(id=id)
        print(Ca.name)
        ser=CatogerySerailizer(Ca)
        print(ser.data)
        return Response(ser.data)


class AdminVideos(APIView):
    def post(self,request):
         id=request.data.get("id")
         ca=Trainers.objects.get(id=id)
         vid=Video.objects.filter(id=ca.t_video.id)
         print(vid)
         seri=VideoSerailzer(vid,many=True)
         print(seri)
         return Response(seri.data)
from datetime import date
class Subscriptions(APIView): 
    def post(self,request):
        userid=request.data.get("userid")
        tid=request.data.get("trainerid")
        print(userid,tid)
        t=Trainers.objects.get(id=tid)
        u=UserAccount.objects.get(id=userid)
        payment="Razorpay"
        s=Subscription.objects.filter(user=u,trainer=t)
        print(s)
        if s:
            return Response({"message":"already subscribed"})
        else:
            sd=Subscription.objects.create(user=u,trainer=t,payment_method=payment,date=date.today(),amount=t.course_fee)
            print(userid,tid,payment)
            return Response({"message":"success"})


class SubscribedDetials(APIView):
    def post(self,request):
        us=request.data.get("id")
        s=Subscription.objects.filter(user=us)
        print(s.values_list())
        dat=Subscriptionseri(s,many=True)
        datas = dat.data
        print(s)
        return Response({"mes":"success","data":datas})



class UserTrainerSubscribers(APIView):
    def post(self, request):
        uid = request.data.get("uid")
        print(uid)
        user=UserAccount.objects.get(id=uid)
        subscriptions = Subscription.objects.filter(user=user)
        if subscriptions==[]:
           return Response({"message": "User has no subscriptions"})
        else:
            print("HAII")
            serialized_data = []
            for subscription in subscriptions:
                # Pass the user_id to the serializer
                serializer = Subscriptionseri(subscription, user_id=uid)
                serialized_data.append(serializer.data)
                print(serialized_data)
            return Response(serialized_data, status=status.HTTP_200_OK)
from datetime import *
today = date.today()

class Slot(CreateAPIView):
    def create(self, request):
            tid = request.data.get("uid")
            print(tid)
            tr = Trainers.objects.get(id=tid)
            time = request.data.get("time")
            date_str = request.data.get("date")
            given_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            print(given_date, today)
            if given_date < today:
                return Response({"message": "not valid date"})
            else:
                sa = Appointment.objects.create(trainer=tr, time=time, date=given_date)
                seri = AppoitmentSeri(sa)
                return Response(seri.data)

        
class MySlots(APIView):
    def post(self,request):
        id=request.data.get("tid")
        tr=Trainers.objects.get(id=id)
        sd=Appointment.objects.filter(trainer=tr)
        seri=AppoitmentSeri(sd,many=True)
        return Response(seri.data)



class UserSlotView(APIView):
    
              
            def post(self, request):
                id = request.data.get("tid")
                tr = Trainers.objects.get(id=id)
                Ap = Appointment.objects.filter(trainer=tr)
                
                # Assuming you have access to the current user

                # Filter out appointments that have bookings by the current user
                available_appointments = []
                for appointment in Ap:
                    if not Booking.objects.filter(appointment=appointment).exists():
                        available_appointments.append(appointment)

                if not available_appointments:
                    return Response({"message": "No slots available"}, status=status.HTTP_404_NOT_FOUND)

                apseri = AppoitmentSeri(available_appointments, many=True)
                return Response(apseri.data)
             
        
                
        
from django.shortcuts import get_object_or_404
class BookingSlot(APIView):
    def post(self,request):
        id=request.data.get("id")
        apid=request.data.get("apid")
        app=Appointment.objects.get(id=apid)
        user=UserAccount.objects.get(id=id)
        s=Booking.objects.create(user=user,appointment=app,is_booked=False)
        print(s)
        return Response({"message":"Booked"})
    



    
from datetime import date

class UserBookingStatusView(APIView):
    def post(self, request):
        id = request.data.get("id")
        user = UserAccount.objects.get(id=id)
        bk = Booking.objects.filter(user=user)
        today = date.today()  # Get today's date

        serialized_data = []
        for subscription in bk:
            appointment_date = subscription.appointment.date
            if appointment_date >= today:
                serializer = BookingSeri(subscription)

                serialized_data.append(serializer.data)
                print(serialized_data)

        return Response(serialized_data)
 



from datetime import datetime

class MyUsersStatus(APIView):
    def post(self, request):
        id = request.data.get("id")
        trainer = Trainers.objects.get(id=id)
        bookings = Booking.objects.filter(appointment__trainer=trainer)
        
        if bookings:
            serialized_bookings = []
            current_date = datetime.now().date()  # Get the current date
            
            for booking in bookings:
                appointment_date = booking.appointment.date
                if appointment_date >= current_date:
                    serialized_booking = {
                        'user_id': booking.user.id,
                        'user_name': booking.user.name,
                        'appointment_time': booking.appointment.time.strftime('%H:%M:%S'),
                        'appointment_date': appointment_date.strftime('%Y-%m-%d'),
                    }
                    serialized_bookings.append(serialized_booking)
            
            if serialized_bookings:
                print("yes")
                return Response(serialized_bookings)
            else:
                print("No")
                return Response({"message": "No future bookings"})
        else:
            print("no")
            return Response({"message": "No bookings"})



    
            
class ChangeStatusofUser(APIView):
    def post(self,request):
            id = request.data.get("tid")
            tr = get_object_or_404(Trainers, id=id)
            Ap = get_object_or_404(Appointment, trainer=tr)
            bk = get_object_or_404(Booking, appointment=Ap)
            bk.is_booked = True
            bk.save()
            bk=get_object_or_404(Booking, appointment=Ap)
            bookings = Booking.objects.filter(appointment__trainer=tr)
            serialized_bookings = []
            for booking in bookings:
                serialized_booking = {
                    'user_id': booking.user.id,
                    'user_name': booking.user.name,
                    'appointment_time': booking.appointment.time.strftime('%H:%M:%S'),
                    'appointment_date': booking.appointment.date.strftime('%Y-%m-%d'),
                    'is_booked': booking.is_booked,
                }
                serialized_bookings.append(serialized_booking)
            print(serialized_bookings)
            return Response(serialized_bookings, status=status.HTTP_200_OK)      
class TrainerChangeStatus(APIView):
    def post(self,request):
            id = request.data.get("tid")
            tr = get_object_or_404(Trainers, id=id)
            Ap = get_object_or_404(Appointment, trainer=tr)
            bk = get_object_or_404(Booking, appointment=Ap)
            bk.is_booked = True
            bk.save()
            bk=get_object_or_404(Booking, appointment=Ap)
            bookings = Booking.objects.filter(appointment__trainer=tr)
            serialized_bookings = []
            for booking in bookings:
                serialized_booking = {
                    'user_id': booking.user.id,
                    'user_name': booking.user.name,
                    'appointment_time': booking.appointment.time.strftime('%H:%M:%S'),
                    'appointment_date': booking.appointment.date.strftime('%Y-%m-%d'),
                    'is_booked': booking.is_booked,
                }
                serialized_bookings.append(serialized_booking)
            print(serialized_bookings)
            return Response(serialized_bookings, status=status.HTTP_200_OK)
    
class AdminBookingStatusView(APIView):
    def get(self, request):
        bookings = Booking.objects.all()
        combined_data=BookingSeri(bookings,many=True)
        print(combined_data.data)
        return Response(combined_data.data)
    
class AdminAppointmentview(APIView):
    def get(self,request):
        A=Appointment.objects.all()
        As=AppoitmentSeri(A,many=True)
        print(As)
        return Response(As.data)

class MySubscribers(APIView):
    def post(self,request):
        id=request.data.get("tid")
        tr=Trainers.objects.get(id=id)
        sub=Subscription.objects.filter(trainer=tr)
        subseri=Subscriptionseri(sub,many=True)
        print(subseri.data)
        return Response(subseri.data)
    
from django.db.models import *
from django.db.models.functions import TruncMonth

class DashBoard(APIView):
    def get(self,request):
        di={}
        user=UserAccount.objects.all()
        trainer=Trainers.objects.all()
        # sub=Subscription.objects.all()
        # subscriptions = Subscription.objects.all()
        # subscriptions = subscriptions.filter(date__isnull=False)  
        # subscriptions = subscriptions.annotate(
        #     month=Sum('amount'),  
        #     year_month=TruncMonth('date') 
        # )
        # monthly_totals = subscriptions.values('year_month').annotate(total_amount=Sum('amount')).order_by('year_month')
        # for i in monthly_totals:
        #     if i in di:
        #      di[i['year_month']]+=i['total_amount']
        #     else:
        #         di[i['year_month']]=i['total_amount']
        monthly_data = (
        Subscription.objects
        .annotate(month=TruncMonth('date'))
        .values('month')
        .annotate(total_amount=Sum('amount'))
        .order_by('month')
    )
        months = [entry['month'].strftime('%B %Y') for entry in monthly_data]
        total_amounts = [entry['total_amount'] for entry in monthly_data]

        data = {
            'months': months,
            'total_amounts': total_amounts,
        }
        d=[]
        s=[]
        for i in user:
            if  i.is_admin==False:
                s.append(i.id)
        for i in trainer:
            d.append(i.id)
            
        m=len(d)
        n=len(s)
        return  Response({"m":m,"n":n,"data":data})
        

class TrainerReviews(CreateAPIView):
    def create(self,request):
        tid=request.data.get("tid")
        uid=request.data.get("uid")
        rating=request.data.get("rating")
        review=request.data.get("review")
        t=Trainers.objects.get(id=tid)
        u=UserAccount.objects.get(id=uid)
        print(t,u,rating,review)
        d=TrainerReview.objects.filter(t_trainer=t,t_user=u)
        if not d:
            if rating!=None and review!=None:
                s=TrainerReview.objects.create(t_trainer=t,t_user=u,rating=rating,review_text=review)
                seri=TrainerReviewSeri(s)
                return Response({"message":"review and rating added"})
            else:
                if rating ==None and review!=None:
                    s=TrainerReview.objects.create(t_trainer=t,t_user=u,review_text=review)
                    seri=TrainerReviewSeri(s)
                    return Response({"message":"review added"})
                if rating !=None and review==None:
                    s=TrainerReview.objects.create(t_trainer=t,t_user=u,rating=rating)
                    seri=TrainerReviewSeri(s)
                    return Response({"message":"rating added"})
        else:
            return Response({"message":"already added"})

class ReviewDetails(APIView):
    def post(self, request):
        tid = request.data.get("id")
        uid=request.data.get("uid")
        try:
            u=UserAccount.objects.get(id=uid)
            t = Trainers.objects.get(id=tid)
            sub=Subscription.objects.get(user=u,trainer=t)
            s = TrainerReview.objects.filter(t_trainer=t)
            ser=Subscriptionseri(sub)
            print(ser)
            if s:
                ratings = 0
                c = 0
                for i in s:
                    ratings += i.rating
                    c += 1
                m = ratings // c
                seri = TrainerReviewSeri(s, many=True)
                return Response({"data": seri.data, "message": m,"sub":ser.data})  
            else:
                return Response({"message": "No review","sub":ser.data}) 
        except:
              return Response({"message": "No query availble"}) 


class Earnings(APIView):
    def post(self,request):
        tid = request.data.get("id")
        t = Trainers.objects.get(id=tid)
        money=0
        sub=Subscription.objects.filter(trainer=t)
        for i in sub:
            money+=i.amount
        return Response({"money":money})


class Myvideos(APIView):
    def post(self,request):
            tid = request.data.get("id")
            print(tid)
            t = Trainers.objects.get(id=tid)
            print(t)
            tsr=Video.objects.get(id=t.t_video.id)
            print(tsr)
            vi=VideoSerailzer(tsr)
            print(vi)
            return Response(vi.data)

class VideoChatLink(APIView):
    def post(self,request):
        email=request.data.get("email")
        link=request.data.get("link")
        send_mail(
            'OTP Verification',
            f'Your OTP is: {link}',
            "settings.EMAIL_HOST_USER",  
            [email],
            fail_silently=False,
        ) 
        return Response({"message":"link send successfully"})
        


    
