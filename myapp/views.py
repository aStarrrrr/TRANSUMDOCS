from pathlib import Path
from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
from .models import *
import datetime
from django.core.files.storage import FileSystemStorage
from email.mime.text import MIMEText
from django.core.mail import send_mail
from django.conf import settings
import random
import smtplib
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
import random
from django.shortcuts import render
from pypdf import PdfReader
from io import BytesIO
from transformers import pipeline
from summarizer import Summarizer  
import pytesseract
from PIL import Image
from io import BytesIO
from django.core.files.storage import FileSystemStorage
from .models import File  
from summarizer import Summarizer
# import fitz

from django.http import HttpResponse
from django.shortcuts import render
from pathlib import Path
# import fitz 








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

# def register(request):
#     if request.method == 'POST' and 'submit' in request.POST:
#         # Generate a random OTP
#         otp = random.randint(1000, 9999)
#         request.session['otp'] = str(otp)  # Save OTP in session
#         print(otp,"oooooootttttttttpppppppppp")
#         # Retrieve form data
#         username = request.POST['username']
#         password = request.POST['password']
#         first_name = request.POST['fname']
#         last_name = request.POST['lname']
#         email1 = request.POST['email']
#         phone = request.POST['phone']

#         request.session["username"]=username
#         request.session["password"]=password
#         request.session["fname"]=first_name
#         request.session["lname"]=last_name
#         request.session["email"]=email1
#         request.session["phone"]=phone

#         # Save the user and login details
       
#         # Prepare and send email
#         # subject = 'Your OTP for Registration'
#         # message = f"""
#         # Thank you for registering!
        
#         # Please use the following OTP to verify your account:
#         # - OTP: {otp}
#         # """
#         # from_email = settings.EMAIL_HOST_USER
#         # recipient_list = [email1]
#         # print(recipient_list,"-----------------------------------------")

#         # try:
#         #     send_mail(subject, message, from_email, recipient_list)
#         # except Exception as e:
#         #     return HttpResponse(f"<script>alert('Error sending email: {e}');window.location='/register';</script>")

#         # return HttpResponse("<script>alert('OTP sent to your email. Please verify.');window.location='/otp_for_registration';</script>")


#         from django.core.mail import send_mail
#     from django.conf import settings

#     subject = 'Test Email'
#     message = f"""
#     This is a test email from Django.

#     Here are the details:
#     - Username: {otp}
   
#     """    
#     from_email = settings.EMAIL_HOST_USER
#     recipient_list = [email1]

#     try:
#         send_mail(subject, message, from_email, recipient_list)
#         return HttpResponse("<script>alert('OTP sent to your email. Please verify.');window.location='/otp_for_registration';</script>")
#     except Exception as e:
#         return HttpResponse(f"<script>alert('Error sending email: {e}');window.location='/register';</script>")


#         # Success message





#     return render(request, 'public/register.html')




def register(request):
    if request.method == 'POST' and 'submit' in request.POST:
        # Generate a random OTP
        otp = random.randint(1000, 9999)
        request.session['otp'] = str(otp)  # Save OTP in session
        print(otp, "oooooootttttttttpppppppppp")

        # Retrieve form data
        username = request.POST['username']
        password = request.POST['password']
        first_name = request.POST['fname']
        last_name = request.POST['lname']
        email1 = request.POST['email']

        # Save data in session for later use
        request.session["username"] = username
        request.session["password"] = password
        request.session["fname"] = first_name
        request.session["lname"] = last_name
        request.session["email"] = email1


        subject = 'Code for TransumDocs'
        message = f'Otp : {otp}'
        recipient_list = [email1]  # Assuming 'email' is the field storing the college's email

        send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list)

        return HttpResponse(""" <script> alert('Code Generated and emailed');window.location='/otp_for_registration'</script>""")


        # # Prepare and send email
        # subject = 'Test Email'
        # message = f"""
        # This is a test email from Django.

        # Here are the details:
        # - Username: {username}
        # - OTP: {otp}
        # """
        # from_email = settings.EMAIL_HOST_USER
        # recipient_list = [email1]

        # try:
        #     send_mail(subject, message, from_email, recipient_list)
        #     return HttpResponse("<script>alert('OTP sent to your email. Please verify.');window.location='/otp_for_registration';</script>")
        # except Exception as e:
        #     return HttpResponse(f"<script>alert('Error sending email: {e}');window.location='/otp_for_registration';</script>")

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
        q1 = Login(username=username, password=password, user_type='user')
        q1.save()

        q2 = User(first_name=first_name, last_name=last_name, email=email1, LOGIN_id=q1.pk)
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

# def user_home(request):
#     if request.session.get('log') == 'out':
#         return HttpResponse(
#             "<script>alert('please login');window.location='login'</script>"
#         )

#     userid = request.session.get('user_id')
#     user = User.objects.get(id=userid)

#     if 'submit' in request.POST:
#         file = request.FILES['input_file']

#         fs = FileSystemStorage()
#         filename = fs.save(file.name, file)
#         file_path = fs.path(filename)

#         try:
#             text = ""
#             with fitz.open(file_path) as pdf:
#                 for page_num in range(len(pdf)):
#                     text += pdf[page_num].get_text()
#             print(text)
#             return HttpResponse(
#                 f"<script>alert('File processed successfully');window.location='user_home'</script>"
#             )
#         except Exception as e:
#             print(f"Error processing file: {e}")
#             return HttpResponse(
#                 f"<script>alert('Error processing file: {e}');window.location='user_home'</script>"
#             )
#         finally:
#             fs.delete(filename)

#     return render(request, 'user/user_home.html', {'user': user})

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
    # if request.session['log']=='out':
    #     return HttpResponse(f"<script>alert('please login');window.location='login'</script>")
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
        # if request.session['log']=='out':
        #     return HttpResponse(f"<script>alert('please login');window.location='login'</script>")
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


from io import BytesIO
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from PyPDF2 import PdfReader  # Alternatively, use fitz (PyMuPDF) or pdfplumber for better extraction
from summarizer import Summarizer  # Extractive summarizer

# def user_home(request):
#     userid = request.session['user_id']
#     user = User.objects.get(id=userid)
    
#     extracted_text = None  # Variable to hold the extracted text
#     summarized_text = None  # Variable to hold the summarized text

#     if request.method == 'POST' and 'pdf_file' in request.FILES:
#         # Get the uploaded PDF file
#         uploaded_file = request.FILES['pdf_file']

#         try:
#             # Read the file into memory (using BytesIO)
#             pdf_path = BytesIO(uploaded_file.read())

#             # Create a PdfReader object from the file object
#             reader = PdfReader(pdf_path)

#             # Extract text from all pages
#             extracted_text = ""
#             for page_number in range(len(reader.pages)):
#                 page = reader.pages[page_number]
#                 text = page.extract_text()
#                 extracted_text += text.strip() + "\n"

#             # Summarize using BERT (Extractive Summarizer)
#             model = Summarizer()  # Load the BERT extractive summarizer model

#             if extracted_text:
#                 # Summarize the extracted text
#                 summarized_text = model(extracted_text, min_length=50, max_length=500)

#                 # Save file and summary to the database
#                 q1 = File(USER_id=userid, file=uploaded_file, output_summary=summarized_text, output_translated='pending')
#                 q1.save()

#         except Exception as e:
#             print(f"Error processing the PDF: {e}")
#             return render(request, 'user/user_home.html', {
#                 'user': user,
#                 'error': "There was an issue processing your PDF file. Please try again."
#             })

#     # Pass both extracted text and summarized text to the template
#     return render(request, 'user/user_home.html', {
#         'user': user,
#         'extracted_text': extracted_text,
#         'summarized_text': summarized_text
#     })








pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# def upload_img(request):
#     userid = request.session['user_id']
#     user = User.objects.get(id=userid)

#     extracted_text = None  # Variable to hold the extracted text from the image
#     summarized_text = None  # Variable to hold the summarized text

#     if request.method == 'POST':
#         if 'image_file' in request.FILES:
#             # Handle image file (e.g., JPG, PNG)
#             uploaded_image = request.FILES['image_file']

#             # Read the image file into memory (using BytesIO)
#             image_path = BytesIO(uploaded_image.read())

#             # Use Pillow to open the image
#             image = Image.open(image_path)

#             # Extract text from the image using pytesseract
#             extracted_text = pytesseract.image_to_string(image)

#             print("Extracted Text from Image:")
#             print(extracted_text)

            
#             model = Summarizer()  

#             if extracted_text:
#                 summarized_text = model(extracted_text)
#                 print("Summarized Text from Image:")
#                 print(summarized_text)

#                 # Save the summarized text and the file to the database (optional)
#                 fs = FileSystemStorage()
#                 fp = fs.save(uploaded_image.name, uploaded_image)
#                 q1 = File(USER_id=userid, file=fs.url(fp), output_summary=summarized_text, output_translated='pending')
#                 q1.save()

#     # Pass the extracted text and summarized text to the template
#     return render(request, 'user/upload_img.html',{
#         'user': user,
#         'extracted_text': extracted_text,
#         'summarized_text': summarized_text }
#     )






# def process_file(request):
#     userid = request.session['user_id']
#     user = User.objects.get(id=userid)

#     summarized_text = None
#     extracted_text = None

#     if request.method == 'POST' and 'input_file' in request.FILES:
#         uploaded_file = request.FILES['input_file']
#         file_type = uploaded_file.content_type

#         try:
#             if file_type.startswith('image/'):  # Check if it's an image file
#                 # Image processing logic
#                 image_path = BytesIO(uploaded_file.read())
#                 image = Image.open(image_path)
#                 extracted_text = pytesseract.image_to_string(image)

#                 model = Summarizer()
#                 if extracted_text:
#                     summarized_text = model(extracted_text)

#             elif file_type == 'application/pdf':  # Check if it's a PDF file
#                 # PDF processing logic
#                 pdf_path = BytesIO(uploaded_file.read())
#                 reader = PdfReader(pdf_path)

#                 extracted_text = ""
#                 for page in reader.pages:
#                     extracted_text += page.extract_text().strip() + "\n"

#                 model = Summarizer()
#                 if extracted_text:
#                     summarized_text = model(extracted_text, min_length=50, max_length=500)

#             # Save the file and summary to the database
#             fs = FileSystemStorage()
#             file_path = fs.save(uploaded_file.name, uploaded_file)
#             q1 = File(USER_id=userid, file=fs.url(file_path), output_summary=summarized_text, output_translated='pending')
#             q1.save()

#         except Exception as e:
#             print(f"Error processing file: {e}")
#             return render(request, 'user/user_home.html', {
#                 'user': user,
#                 'error': "There was an issue processing your file. Please try again."
#             })

#     return render(request, 'user/user_home.html', {
#         'user': user,
#         'extracted_text': extracted_text,
#         'summarized_text': summarized_text
#     })













#----------------------------------------------------------------------------------------------------------------------------











def process_file(request):
    userid = request.session['user_id']
    user = User.objects.get(id=userid)

    summarized_text = None
    extracted_text = None

    if request.method == 'POST' and 'input_file' in request.FILES:
        uploaded_file = request.FILES['input_file']
        file_type = uploaded_file.content_type

        try:
            if file_type.startswith('image/'):  # Check if it's an image file
                # Image processing logic
                image_path = BytesIO(uploaded_file.read())
                image = Image.open(image_path)
                extracted_text = pytesseract.image_to_string(image)

                model = Summarizer()
                if extracted_text:
                    summarized_text = model(extracted_text, min_length=100)

            elif file_type == 'application/pdf':  # Check if it's a PDF file
                # PDF processing logic
                pdf_path = BytesIO(uploaded_file.read())
                reader = PdfReader(pdf_path)

                extracted_text = ""
                for page in reader.pages:
                    extracted_text += page.extract_text().strip() + "\n"

                model = Summarizer()
                if extracted_text:
                    summarized_text = model(extracted_text, min_length=50, max_length=500)

            # Save the file and summary to the database
            fs = FileSystemStorage()
            file_path = fs.save(uploaded_file.name, uploaded_file)

            # Save the file URL in the session
            request.session['uploaded_file_url'] = fs.url(file_path)
            
            q1 = File(USER_id=userid, file=fs.url(file_path), output_summary=summarized_text, output_translated='pending')
            q1.save()

        except Exception as e:
            print(f"Error processing file: {e}")
            return render(request, 'user/user_home.html', {
                'user': user,
                'error': "There was an issue processing your file. Please try again."
            })

    # Retrieve the file URL from the session if available
    uploaded_file_url = request.session.get('uploaded_file_url')

    return render(request, 'user/user_home.html', {
        'user': user,
        'extracted_text': extracted_text,
        'summarized_text': summarized_text,
        'uploaded_file_url': uploaded_file_url
    })






#------------------------------------------------------------------------------------------------------------------









# def process_file(request):
#     from io import BytesIO
#     from django.core.files.storage import FileSystemStorage
#     from PyPDF2 import PdfReader
#     from PIL import Image
#     from transformers import pipeline
#     import pytesseract
#     import logging

#     # Configure logging
#     logging.basicConfig(level=logging.INFO)

#     # Specify the path to the Tesseract executable
#     pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

#     userid = request.session['user_id']
#     user = User.objects.get(id=userid)

#     summarized_text = None
#     extracted_text = None

#     if request.method == 'POST' and 'input_file' in request.FILES:
#         uploaded_file = request.FILES['input_file']
#         file_type = uploaded_file.content_type

#         try:
#             logging.info("Starting file processing...")
#             # File storage initialization
#             fs = FileSystemStorage()
#             file_path = fs.save(uploaded_file.name, uploaded_file)
#             request.session['uploaded_file_url'] = fs.url(file_path)

#             if file_type.startswith('image/'):  # Check if it's an image file
#                 logging.info("Processing an image file...")
#                 image_path = BytesIO(uploaded_file.read())
#                 image = Image.open(image_path)
#                 extracted_text = pytesseract.image_to_string(image)

#             elif file_type == 'application/pdf':  # Check if it's a PDF file
#                 logging.info("Processing a PDF file...")
#                 pdf_path = BytesIO(uploaded_file.read())
#                 reader = PdfReader(pdf_path)

#                 # Process PDF in chunks (page-by-page)
#                 extracted_text = ""
#                 for page_num, page in enumerate(reader.pages):
#                     if page_num % 10 == 0:
#                         logging.info(f"Processing page {page_num + 1}...")
#                     extracted_text += page.extract_text().strip() + "\n"

#             # Summarize text if extraction was successful
#             if extracted_text:
#                 logging.info("Starting text summarization...")
#                 model = pipeline("summarization")
#                 chunk_size = 1000  # Characters
#                 chunks = [extracted_text[i:i + chunk_size] for i in range(0, len(extracted_text), chunk_size)]

#                 summarized_text = ""
#                 for chunk in chunks:
#                     summarized_text += model(chunk, min_length=50, max_length=500)[0]['summary_text'] + "\n"

#             # Save file and summary to the database
#             q1 = File(USER_id=userid, file=fs.url(file_path), output_summary=summarized_text, output_translated='pending')
#             q1.save()

#         except Exception as e:
#             logging.error(f"Error processing file: {e}")
#             return render(request, 'user/user_home.html', {
#                 'user': user,
#                 'error': "There was an issue processing your file. Please try again."
#             })

#     # Retrieve the file URL from the session if available
#     uploaded_file_url = request.session.get('uploaded_file_url')

#     return render(request, 'user/user_home.html', {
#         'user': user,
#         'extracted_text': extracted_text,
#         'summarized_text': summarized_text,
#         'uploaded_file_url': uploaded_file_url
#     })
