from pathlib import Path
from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
from .models import*
import datetime
from django.core.files.storage import FileSystemStorage
from email.mime.text import MIMEText
from django.core.mail import send_mail
from django.conf import settings
import random
import smtplib
import fitz

from django.http import HttpResponse
from django.shortcuts import render
from pathlib import Path
import fitz 

def login(request):
    request.session['log']="out"
    if 'submit' in request.POST:
        username = request.POST['username']
        password = request.POST['password']
        if Login.objects.filter(username=username,password=password).exists():
            res = Login.objects.get(username=username,password=password)
            request.session['login_id']=res.pk
            login_id=request.session['login_id']

            if res.user_type =='admin':
                request.session['log']="in"
                
                return HttpResponse(f"<script>alert('welcome Admin');window.location='admin_home'</script>")

            elif res.user_type =='user':
               

                if User.objects.filter(LOGIN_id=login_id).exists():
                    res2=User.objects.get(LOGIN_id=login_id)
                    if res2:
                        request.session['user_id']=res2.pk
                        request.session['log']="in"
                        return HttpResponse(f"<script>alert('welcome user');window.location='user_home'</script>")
                    else:
                        return HttpResponse(f"<script>alert('invalid user');window.location='login'</script>")
                else:
                        return HttpResponse(f"<script>alert('this user ID  does not exist');window.location='login'</script>")

            elif res.user_type =='blocked':
                return HttpResponse(f"<script>alert('you are blocked by admin');window.location='/login'</script>")

            elif res.user_type =='pending':
                return HttpResponse(f"<script>alert('you are not approved by admin....please wait for approval');window.location='/login'</script>")
            
            else:
                return HttpResponse(f"<script>alert('invalid user ');window.location='login'</script>")

        else:
            return HttpResponse(f"<script>alert('invalid username or password');window.location='login'</script>")
    return render(request,'public/login.html')

def dd(request):
    return render(request,"public/login.html")

def register(request):
    if request.method == 'POST' and 'submit' in request.POST:
        # Generate a random OTP
        otp = random.randint(1000, 9999)
        request.session['otp'] = str(otp)  # Save OTP in session
        print(otp,"oooooootttttttttpppppppppp")

        # Retrieve form data
        username = request.POST['username']
        password = request.POST['password']
        first_name = request.POST['fname']
        last_name = request.POST['lname']
        email1 = request.POST['email']
        phone = request.POST['phone']

        request.session["username"]=username
        request.session["password"]=password
        request.session["fname"]=first_name
        request.session["lname"]=last_name
        request.session["email"]=email1
        request.session["phone"]=phone

        # Save the user and login details
       
        # Prepare and send email
        subject = 'Your OTP for Registration'
        message = f"""
        Thank you for registering!
        
        Please use the following OTP to verify your account:
        - OTP: {otp}
        """
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [email1]

        try:
            send_mail(subject, message, from_email, recipient_list)
        except Exception as e:
            return HttpResponse(f"<script>alert('Error sending email: {e}');window.location='/register';</script>")

        return HttpResponse("<script>alert('OTP sent to your email. Please verify.');window.location='/otp_for_registration';</script>")

    return render(request, 'public/register.html')

def otp_for_registration(request):
        return render(request, 'public/otp_for_registration.html')

def otp_for_registration_post(request):
    user_otp = request.POST['otpS']  # User-entered OTP
    session_otp = request.session['otp']  # OTP stored in session
    print(user_otp,session_otp)
    # Validate OTP
    if str(user_otp) == str(session_otp):
        username=request.session["username"]
        password=request.session["password"]
        first_name=request.session["fname"]
        last_name=request.session["lname"]
        email1=request.session["email"]
        phone=request.session["phone"]
        q1 = Login(username=username, password=password, user_type='user')
        q1.save()

        q2 = User(first_name=first_name, last_name=last_name, email=email1, phone=phone, LOGIN_id=q1.pk)
        q2.save()
        return HttpResponse("<script>alert('Verification successful');window.location='/login';</script>")
    else:
        return HttpResponse("<script>alert('Invalid OTP. Please try again.');window.location='/otp_for_registration';</script>")
    
def admin_home(request):

    if request.session['log']=="out":
        return HttpResponse(f"<script>alert('please login');window.location='login'</script>")

    return render(request,'admin/admin_home.html')

def admin_manage_users(request):
    if request.session['log']=='out':
        return HttpResponse(f"<script>alert('please login');window.location='login'</script>")
    data = User.objects.all()
    return render(request,'admin/manage_users.html',{'data':data})

def admin_block_user(request,id):
    if request.session['log']=='out':
        return HttpResponse(f"<script>alert('please login');window.location='login'</script>")
    data = Login.objects.get(id=id)
    data.user_type = 'blocked'
    data.save()
    return HttpResponse(f"<script>alert('Succesfully blocked');window.location='/admin_manage_user'</script>")

def admin_unblock_user(request,id):
    if request.session['log']=='out':
        return HttpResponse(f"<script>alert('please login');window.location='login'</script>")
    data = Login.objects.get(id=id)
    data.user_type = 'user'
    data.save()
    return HttpResponse(f"<script>alert('Succesfully unblocked');window.location='/admin_manage_user'</script>")

def admin_view_feedback(request):
    if request.session['log']=='out':
        return HttpResponse(f"<script>alert('please login');window.location='login'</script>")
    data = Feedback.objects.all()
    return render(request,'admin/admin_view_feedback.html',{'data':data})

def admin_view_complaints(request):
    if request.session['log']=='out':
        return HttpResponse(f"<script>alert('please login');window.location='login'</script>")
    data = Complaint.objects.all()
    return render(request,'admin/admin_view_complaints.html',{'data':data})

def admin_complaint_reply(request,id):
    if request.session['log']=='out':
        return HttpResponse(f"<script>alert('please login');window.location='login'</script>")
    data = Complaint.objects.get(id=id)
    if 'submit' in request.POST:
        reply = request.POST['reply']
        data.reply = reply
        data.save()
        return HttpResponse(f"<script>alert('Reply submitted');window.location='/admin_view_complaints'</script>")
    return render(request,'admin/admin_complaint_reply.html',{'data':data})

def user_header(request ):
    userid = request.session['user_id']
    user=User.objects.get( id=userid)
    return render(request,'user/user_header.html' , {'user':user})

# def user_home(request ):
#     if request.session['log']=='out':
#         return HttpResponse(f"<script>alert('please login');window.location='login'</script>")
#     userid = request.session['user_id']
#     user=User.objects.get( id=userid)
#     if 'submit' in request.POST:
#         file = request.FILES['input_file']

#         import datetime
#         file_extension = Path(file.name).suffix  
#         if not file_extension:  
#             file_extension = ".bin" 
#         date = datetime.datetime.now().strftime("%Y%m%d-%H%M%S") + file_extension
#         fs = FileSystemStorage() 
#         fp = fs.save(date, file)

#         text = ""
#         with fitz.open(file) as pdf:
#             for page_num in range(len(pdf)):
#                 text += pdf[page_num].get_text()
#             return text
#         print(text)

#         # import datetime
#         # file_extension = Path(file.name).suffix  
#         # if not file_extension:  
#         #     file_extension = ".bin" 
#         # date = datetime.datetime.now().strftime("%Y%m%d-%H%M%S") + file_extension
#         # fs = FileSystemStorage() 
#         # fp = fs.save(date, file)

#         # q1 = File(USER_id=userid,file=fs.url(fp),output_summary='pending',output_translated='pending')
#         # q1.save()

#         return HttpResponse(f"<script>alert('File uploaded');window.location='user_home'</script>")
#     return render(request,'user/user_home.html' , {'user':user})

def user_home(request):
    if request.session.get('log') == 'out':
        return HttpResponse(
            "<script>alert('please login');window.location='login'</script>"
        )

    userid = request.session.get('user_id')
    user = User.objects.get(id=userid)

    if 'submit' in request.POST:
        file = request.FILES['input_file']

        fs = FileSystemStorage()
        filename = fs.save(file.name, file)
        file_path = fs.path(filename)

        try:
            text = ""
            with fitz.open(file_path) as pdf:
                for page_num in range(len(pdf)):
                    text += pdf[page_num].get_text()
            print(text)
            return HttpResponse(
                f"<script>alert('File processed successfully');window.location='user_home'</script>"
            )
        except Exception as e:
            print(f"Error processing file: {e}")
            return HttpResponse(
                f"<script>alert('Error processing file: {e}');window.location='user_home'</script>"
            )
        finally:
            fs.delete(filename)

    return render(request, 'user/user_home.html', {'user': user})

def user_view_profile(request):
    if request.session['log']=='out':
        return HttpResponse(f"<script>alert('please login');window.location='login'</script>")
    userid = request.session['user_id']
    data = User.objects.get(id=userid)
    return render(request,'user/view_profile.html',{'data':data})

def user_feedback(request):
    if request.session['log']=='out':
        return HttpResponse(f"<script>alert('please login');window.location='login'</script>")
    userid = request.session['user_id']
    user=User.objects.get( id=userid)
    if 'submit' in request.POST:
        feedback = request.POST['feedback']

        q1 = Feedback(feedback=feedback,USER_id=userid)
        q1.save()

        return HttpResponse(f"<script>alert('Feedback submitted');window.location='/user_feedback'</script>")

    return render(request,'user/user_feedback.html' , {'user':user})

def user_complaints(request):
    print(request.session['log'])
    if request.session['log']=='out':       
        # return HttpResponse(f"""<script>alert('You haven't logged in yet'); window.location='/login';</script>""")
        return HttpResponse(f"<script>alert('please login');window.location='login'</script>")
    userid = request.session['user_id']
    data = Complaint.objects.filter(USER_id=userid)
    user=User.objects.get( id=userid)
    if 'submit' in request.POST:
        complaint = request.POST['complaint']

        q1 = Complaint(complaint=complaint,reply='pending',USER_id=userid)
        q1.save()

        return HttpResponse(f"<script>alert('Complaint submitted');window.location='/user_complaints'</script>")

    return render(request,'user/user_complaints.html',{'data':data , 'user':user})

def user_change_password(request):
    if request.session['log']=='out':
        return HttpResponse(f"<script>alert('please login');window.location='login'</script>")
    # if request.session['log']=="out":
    #     return HttpResponse(f"<script>alert('You havent logged in yet...!');window.location='/login'</script>")
    login_id=request.session['login_id']
    q=Login.objects.get(id=login_id)
    if 'submit' in request.POST:
        old_password=request.POST['old_password']
        if Login.objects.filter(id=login_id ,password=old_password).exists():
            q.password=request.POST['password']
            q.save()
            return HttpResponse(f"<script>alert('your password changed successfully :)');window.location='user_view_profile'</script>")
        else:
            return HttpResponse(f"<script>alert('user password mis match.. please try again ');window.location='user_view_profile'</script>")
            
    return render(request,'user/user_change_password.html')

def user_files(request):
    if request.session['log']=='out':
        return HttpResponse(f"<script>alert('please login');window.location='login'</script>")
    print(request.session['log'])
    userid = request.session['user_id']
    data = File.objects.filter(USER_id=userid)
    user=User.objects.get( id=userid)

    return render(request,'user/user_files.html',{'data':data , 'user':user})

def user_history(request):
    if request.session['log']=='out':
        return HttpResponse(f"<script>alert('please login');window.location='login'</script>")
    userid = request.session['user_id']
    data = File.objects.filter(USER_id=userid)
    user=User.objects.get( id=userid)

    return render(request,'user/user_history.html',{'data':data , 'user':user})

def otp_for_registration(request):
    return render (request,'public/otp_for_registration.html')

def otp_for_forgot_password(request):
    return render (request,'public/forgot_password2.html')

def otp_entering_page(request):
    return render (request,'public/otp_for_forgot_password.html')

def forgot_password(request):
        if request.session['log']=='out':
            return HttpResponse(f"<script>alert('please login');window.location='login'</script>")
        if 'submit' in request.POST:
            otp=0
            uname=request.POST['uname']
            email=request.POST['email']
            request.session['uname']=uname
            request.session['email']=email
            otp = random.randint(1000, 9999)
            request.session['otp']=otp
            subject = 'Your OTP for Registration'
            message = f"""
            Thank you for registering!
            
            Please use the following OTP to verify your account:
            - OTP: {otp}
            """
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [email]

        try:
            send_mail(subject, message, from_email, recipient_list)
        except Exception as e:
            return HttpResponse(f"<script>alert('Error sending email: {e}');window.location='/login';</script>")

        return render(request,'public/otp_for_forgot_password.html')

def otp_post_forgot(request): 
    uname=request.session['uname']
    email=request.session['email']
    otpS=request.POST['otpS']
    # print (request.session['otp'])
    # print(otpS)
    if int(request.session['otp']) == int(otpS):
        #     # q="update login set password='%s' where username='%s'"%(password,uname)
        #     # update(q)
        # q=Login.objects.get(username=uname)
        # q.password=password
        # q.save()
        # return "<script>alert('Password changed');window.location='/login'</script>"
    # else:
    #     return "<script>alert('OTP desnot match');window.location='/login'</script>"
        return render(request, 'public/set_new_password.html')
        # return HttpResponse("<script>alert('Invalid OTP. Please try again.');window.location='/otp_for_registration';</script>")
    else:
        # Return an error message and redirect to login page
        return HttpResponse("<script>alert('Invalid OTP. Please try again.');window.location='/otp_entering_page';</script>")
    
def change_password_on_forgot_password(request):
    if request.method == 'POST':
        uname=request.session.get('uname')
        password=request.POST.get('password')
        if not uname or not password:
            return render(request, 'public/login.html', {"error": "Invalid request or missing data"})
        try:
            q = Login.objects.get(username=uname)
            q.password = password  # Update the password
            q.save()
            return HttpResponse(f"<script>alert('Password changed successfully');window.location='/login'</script>")
        except Login.DoesNotExist:
            return HttpResponse(f"<script>alert('User not found');window.location='/login'</script>")
    else:
        return HttpResponse(f"<script>alert('Invalid request method');window.location='/login'</script>")

def logout(request):
    request.session['log']="out"
    return HttpResponse(f"<script>alert('Logged out');window.location='/login'</script>")

# def extract_text_from_pdf(pdf_path):
#     text = ""
#     with fitz.open(pdf_path) as pdf:
#         for page_num in range(len(pdf)):
#             text += pdf[page_num].get_text()
#     return text