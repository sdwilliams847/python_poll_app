from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Question, Option, Answer

def index(request):
    return render(request, 'poll_forum/index.html')

def register(request):
    response = User.objects.register(
        first_name = request.POST['first_name'],
        last_name = request.POST['last_name'],
        email = request.POST['email'],
        password = request.POST['password'],
        confirm_password = request.POST['confirm_password']
    )

    if response['valid']:
        request.session["user_id"] = response['user'].id
        return redirect("/forum")
    else: 
        for error in response['errors']:
            messages.error(request, error)
        return redirect('/')

def login(request):
    response = User.objects.login(
        email = request.POST['email'], 
        password = request.POST['password']
    )

    if response['valid']:
        request.session['user_id'] = response['user'].id
        return redirect('/forum')
    
    if len(response['errors']) > 0:
        for error in response['errors']:
            messages.warning(request, error)
        return redirect('/')

def logout(request):
    request.session.flush()
    return redirect('/')

def forum(request):
    if 'user_id' not in request.session:
        messages.add_message(request, messages.ERROR, 'You must log in first!')
        return redirect("/")
    allQ = Question.objects.all()
    userQs = User.objects.get(id=request.session['user_id'])

    userAs = userQs.answers.all()
    arr = []
    for x in userAs:
        arr.append(x.question.id)
        
    for x in arr:
        allQ = allQ.exclude(id=x)

    userQs = Question.objects.all()
    for x in allQ:
        userQs = userQs.exclude(id=x.id)

    data = {
        'question': allQ,
    }
    userQs = userQs.order_by('-id')
    if len(userQs) > 0:
        for Q in userQs:

            Q.option1 = 0
            Q.option2 = 0
            Q.option3 = 0
            Q.option4 = 0

            Q.optionNames = []
            ans = Q.answers.all()
            for option in Q.options.all():
                Q.optionNames.append(option.option)

            for a in ans:
                if a.option.option == Q.optionNames[0]:
                    Q.option1 +=1
                elif a.option.option == Q.optionNames[1]:
                    Q.option2 +=1
                elif a.option.option == Q.optionNames[2]:
                    Q.option3 +=1
                elif a.option.option == Q.optionNames[3]:
                    Q.option4 +=1

        data['userQs'] = userQs


    return render(request, 'poll_forum/forum.html', data)

def create_poll(request):
    return render(request,'poll_forum/create_poll.html')

def newPoll(request):
    if 'user_id' not in request.session:
        messages.add_message(request, messages.ERROR, 'You must log in first!')
        return redirect("/")
    response = {
        "errors": [],
        "valid": False,
    }

    opt1 = request.POST['option1']
    opt2 = request.POST['option2']
    opt3 = request.POST['option3'] 
    opt4 = request.POST['option4']
    
    opt1 = str(opt1)
    opt2 = str(opt2)
    opt3 = str(opt3)
    opt4 = str(opt4)

# how can I rephrase the if statement below to simplify the two answer requirement?
    if (opt1 !="" and opt2 !="") or (opt3 !="" and opt4 !="") or (opt4 !="" and opt1 !="") or (opt2 !="" and opt3 != "") or (opt2 !="" and opt4!="") or (opt3 !="" and opt1 !=""):
        response = Question.objects.newQuestion(
            content = request.POST['content'],
            createdBy = User.objects.get(id=request.session["user_id"]),
        )
    else:
        response["errors"].append("Your question must have at least two possible answers.")


    if response['valid']:   
        if opt1 != "":
            Option.objects.newOption(
                option = opt1,
                relatedQ = response['question'],
            )
        if opt2 != "":
            Option.objects.newOption(
                option = opt2,
                relatedQ = response['question'],
            )
        if opt3 != "":
            Option.objects.newOption(
                option = opt3,
                relatedQ = response['question'],
            )
        if opt4 != "":
            Option.objects.newOption(
                option = opt4,
                relatedQ = response['question'],
            )
        return redirect('/forum')


    if len(response['errors']) > 0:
        for error in response['errors']:
            messages.error(request, error)
        return redirect('/forum')

def process(request, id):
    if 'user_id' not in request.session:
        messages.add_message(request, messages.ERROR, 'You must log in first!')
        return redirect("/")
    
    
    answer = request.POST['ThisTheAnswer']
    Answer.objects.newAnswer(
        question=Question.objects.get(id=id),
        option=Option.objects.get(id=answer),
        answered_by=User.objects.get(id=request.session['user_id'])
    )

    return redirect('/forum')