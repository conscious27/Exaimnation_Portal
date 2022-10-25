from telnetlib import LOGOUT
from django.shortcuts import render, redirect
from django.contrib import messages

# Create your views here.
def exampage(request):

    if request.method == "POST":
        answer1 = request.POST.get("a1")
        answer2 = request.POST.get("a2")
        answer3 = request.POST.get("a3")
        answer4 = request.POST.get("a4")
        answer5 = request.POST.get("a5")
        answer6 = request.POST.get("a6")
        answer7 = request.POST.get("a7")
        answer8 = request.POST.get("a8")
        answer9 = request.POST.get("a9")
        answer10 = request.POST.get("a10")

        count = 0

        if(answer1!=""):
            count +=1
        if(answer2!=""):
            count +=1
        if(answer3!=""):
            count +=1
        if(answer4!=""):
            count +=1
        if(answer5!=""):
            count +=1
        if(answer6!=""):
            count +=1
        if(answer7!=""):
            count +=1
        if(answer8!=""):
            count +=1
        if(answer9!=""):
            count +=1
        if(answer10!=""):
            count +=1

        message = "total marks gained: " + str(count)
        messages.success(request, message)

        return redirect('completion')
    return render(request, 'takeexam/exampage.html')

def completion(request):
    return render(request, 'takeexam/completion.html')