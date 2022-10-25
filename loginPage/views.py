from http.client import HTTPResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from examination import settings
from django.core.mail import send_mail, EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from . tokens import generate_token

# Create your views here.
def home(request):
    return render(request, "loginPage/index.html")

def signup(request):

    if request.method == "POST":
        # username = request.POST.get("Username")
        name = request.POST.get("Name")
        age = request.POST.get("Age")
        university = request.POST.get("University")
        branch = request.POST.get("Branch")
        stream = request.POST.get("Stream")
        email = request.POST.get("Email")
        phone = request.POST.get("Phone")
        username = request.POST.get("Username")
        password = request.POST.get("Password")
        password2 = request.POST.get("Password2")

        if User.objects.filter(username = username):
            messages.error(request, "Username already existss! Try Another!")
            return redirect("home")

        if User.objects.filter(email = email):
            messages.error(request, "E-mail already existss! Try Another!")
            return redirect("home")

        if(len(username) > 15):
            messages.error(request, "Username too big, try less than 15 words")

        if(password != password2):
            messages.error(request, "Password didn't Match!")

        if not username.isalnum():
            messages.error(request, "Username only contain numbers and letters")
        myuser = User.objects.create_user(username, email, password)
        myuser.fname = name
        myuser.age = age
        myuser.university = university
        myuser.branch = branch
        myuser.stream = stream
        myuser.is_active = False
        myuser.phone = phone

        myuser.save()
        messages.success(request, "Your Account has been successfully created. We have sent you a confirmation mail. Please confirm it to activate your account")


        # welcome email

        subject = "WELCOME TO THE EXAMINATION PORTAL!"
        message = "Hello" + myuser.fname + "Happy to see you! May GOD bless you. Please confirm you email address we sent to your account. \n\n Thanking you. \n\n Chaitanya Pradhan"
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, from_email, to_list, fail_silently=False)

        # Email Address through Confirmation mail

        current_site = get_current_site(request)
        email_subject = "Confirm your email!"
        message2 = render_to_string('email_confirmation.html' ,{
            'name' : myuser.fname,
            'domain' : current_site.domain,
            'uid' : urlsafe_base64_encode(force_bytes(myuser.pk)),
            'token' : generate_token.make_token(myuser)
        })
        email = EmailMessage(
            email_subject,
            message2,
            settings.EMAIL_HOST_USER,
            [myuser.email]
        )
        email.fail_silently = True
        email.send()
        return redirect('signin')

    return render(request, "loginPage/signup.html")

def signin(request):

    if request.method == "POST":
        username = request.POST["Username"]
        password = request.POST["Password"]

        user  = authenticate(username = username, password=password)

        if user is not None:
            login(request, user)
            name = username
            return render(request, "loginPage/index.html", {"name":name})

        else:
            messages.error(request, "Wrong Credentials")
            return redirect(home)
    return render(request, "loginPage/signin.html")

def signout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully")
    return redirect(home)

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        myuser = None

    if myuser is not None and generate_token.check_token(myuser, token):
        myuser.is_active = True
        myuser.save()
        login(request, myuser)
        return redirect(home)
    else:
        return render(request, 'activation_failed.html')