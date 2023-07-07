from django.shortcuts import render, redirect
from django.http import HttpResponse
# from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import User, Revenue
from django.core.mail import send_mail, BadHeaderError
from .forms import DateRangeForm, UserForm, MemberForm
import random
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from django.utils import timezone  
from django.db.models import Q  # Add this line to import Q

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.db.models import Q
from datetime import timedelta
from django.utils import timezone
from django.core.paginator import Paginator
User = get_user_model()
from django.shortcuts import get_object_or_404

@login_required(login_url="loginPage")
def home(request):
    query = request.GET.get('query')  # Get the search query from the request
    
    users = User.objects.all()

    # Apply search filter if query exists
    if query:
        users = users.filter(
            Q(id__icontains=query) |
            Q(phone__icontains=query) |
            Q(fee_amount__icontains=query) |
            Q(username__icontains=query)
        )

    today_date = timezone.now().date()
    due_members = []
    members = []
    for member in users:
        if not member.is_staff:
            members.append(member)
            due_date = member.due_date
            if due_date is not None or member.is_fee_paid == 0:
                if due_date:
                    two_days_before_due_date = due_date - timedelta(days=2)
                    if today_date >= two_days_before_due_date:
                        print('Hello, you have to pay the fee: ' + member.username)
                        if today_date >= due_date:
                            member.is_active = False
                            member.is_fee_paid = False
                            due_members.append(member)
                        
                    else:
                        print('Hello, it\'s time to pay the fee: ' + member.username)
                if member.is_fee_paid == 0:
                    if members not in due_members:
                        due_members.append(member)
    print('Total members are: ')
    print(len(members))
    print(len(due_members))
    paginator = Paginator(members, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    print(len(page_obj))
    context = {'members': members, 'due_members': due_members, 'query': query, 'page_obj':page_obj}
    return render(request, 'myauth/home.html', context)

def loginPage(request):
   

    if request.user.is_authenticated:
        return redirect('home')
    if request.method == "POST":
        email = request.POST.get('email').lower()
        password = request.POST.get('password')
        username = request.POST.get('username')
        print("user entered email is "+email)
        print("user entered email is "+password)
    try:
        user = User.objects.get(email=email)
        print("data  email is "+user.email)
        print("data password is "+user.password)
        user_obj = User.objects.get(email=email)
        user = authenticate(email=user_obj.email, password=password)
        print(user)
        if user is not None:
            login(request, user)
            return redirect('home')
    except:
        messages.error(request, "Username OR password is incorrect ")
    return render(request, 'myauth/loginSignupPage.html')


def logoutPage(request):
    logout(request)
    return redirect('loginPage')

# @login_required(login_url="loginPage")
# def registerNewUser(request):
#     if request.method == 'POST':
#         form = MemberForm(request.POST)
#         print('before valid stage ')
#         print(form)

#         if form.is_valid():
#             print('inside valid stage ')
#             user = form.save(commit=False)
#             # user.username=user.username.lower()
#             email = user.email.lower()
#             newUser = User.objects.create_user(email=email, password=None)
#             newUser.username = user.username
#             newUser.phone = user.phone
#             profile_picture = request.FILES.get('profile_pic')
#             newUser.profile_pic = profile_picture
#             newUser.fee_amount = user.fee_amount
#             newUser.is_fee_paid = True
#             today = datetime.now()
#             newUser.fee_paid_date=today
#             due_date = today + relativedelta(months=1)
#             newUser.due_date = due_date
#             newUser.save()
#             if newUser is not None:
#                 return redirect('home')
#         else:
#             messages.error(request, "An error occured during registration.. ")
#     else:
        
#         form = MemberForm()

#     context = {'form': form}
#     return render(request, 'myauth/registerNewUser.html', context)
@login_required(login_url="loginPage")
def registerNewUser(request):
    if request.method == 'POST':
        form = MemberForm(request.POST, request.FILES)
        print('before valid stage ')
        # print(form)

        if form.is_valid():
            print('inside valid stage ')
            user = form.save(commit=False)
            # user.username = user.username.lower()
            email = user.email.lower()
            newUser = User.objects.create_user(email=email, password=None)
            newUser.username = user.username
            newUser.phone = user.phone
            today = datetime.now()
            is_fee_paid = user.is_fee_paid
            profile_picture = request.FILES.get('profile_pic')
            try:
                if profile_picture:
                    newUser.profile_pic = profile_picture
                
                if user.fee_amount:
                    newUser.fee_amount = user.fee_amount                           
                else:
                    newUser.fee_amount = 0.0
                
                if is_fee_paid:
                    newUser.is_fee_paid = True
                    newUser.is_active=True
                    newUser.fee_paid_date = today
                    due_date = today + relativedelta(months=1)
                    newUser.due_date = due_date
                    revenue = Revenue(user=newUser, fee_amount=newUser.fee_amount, submission_date=today, marked_paid_by = request.user)
                    revenue.save()
                    

                if user.blood_group:
                    newUser.blood_group=user.blood_group
                else:
                    newUser.blood_group=""
                
                newUser.added_by = request.user
                newUser.save()
                
                if newUser is not None:
                    
                    return redirect('home')
            except Exception as e:
                # Handle the exception
                messages.error(request, "An error occurred during registration: {}".format(str(e)))
                # You can also log the exception for debugging purposes
                # logger.error("Error occurred during registration: {}".format(str(e)))
        else:
            messages.error(request, "An error occurred during registration..")
    else:
        form = MemberForm()
    print('Form------', form)
    context = {'form': form}
    return render(request, 'myauth/registerNewUser.html', context)



@login_required(login_url="loginPage")
def reports(request):
    total_revenue = 0.0
    if request.method == 'POST':
        form = DateRangeForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            members = Revenue.objects.all()
            for member in members:
                    if end_date >= member.submission_date >= start_date:
                        if member.fee_amount:
                            total_revenue+=float(member.fee_amount)

            # Do something with the selected dates
    else:
        form = DateRangeForm()

    context = {'form': form, 'total_revenue': total_revenue}
    return render(request, 'myauth/reports.html', context)


@login_required(login_url="loginPage")
def getFeePaid(request,pk):
    if request.method == 'POST':
        today = datetime.now()
        fee_amount = request.POST.get('fee_amount')        
        member=User.objects.get(id=pk)
        member.is_fee_paid=True
        member.is_active=True
        member.fee_paid_date=timezone.now()
        if member.due_date is not None:
            due_date=member.due_date
            due_date = due_date + relativedelta(months=1)
        else:
            due_date = today + relativedelta(months=1)
        member.due_date=due_date
        # if fee_amount is not None:
        #     member.fee_paid_amount=fee_amount
        # elif member.fee_paid_amount:
        #     member.fee_paid_amount=0.0
        
        member.added_by = request.user
        member.save()
        revenue = Revenue(user=member, fee_amount=fee_amount, submission_date=today)
        revenue.marked_paid_by = request.user
        revenue.save()
        

        return redirect('dueMembers')
    return redirect('dueMembers')

@login_required(login_url="loginPage")
def deleteMember(request, pk):
    member=User.objects.get(id=pk)
    # member.delete
    if request.method=="POST":
        member.delete()
        return redirect("home")
    
    return render(request, "myauth/delete.html",{'member':member})


@login_required(login_url="loginPage")
def dueMembers(request):   
    due_members=[]
    today_date = timezone.now().date()
    members=User.objects.all()
    for member in members:
        if not member.is_staff:
            due_date = member.due_date
            if due_date is not None or member.is_fee_paid == 0:
                    if due_date:
                        two_days_before_due_date = due_date - timedelta(days=2)
                        if today_date >= two_days_before_due_date:
                            print('Hello, you have to pay the fee: ' + member.username)
                            if today_date >= due_date:
                                member.is_active = False
                                member.is_fee_paid = False
                                due_members.append(member)
                            
                        else:
                            pass
                    if member.is_fee_paid == 0:
                        if members not in due_members:
                            due_members.append(member)
        
    
    paginator = Paginator(due_members, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
      
    context={'page_obj':page_obj}
    return render(request, "myauth/dueMembersComponent.html",context)



@login_required(login_url="loginPage")
def bloodGroup(request):
    query = request.GET.get('query')  # Get the search query from the request
    users = User.objects.filter(is_staff=False)
    # Apply search filter if query exists
    
    if query:
        users = users.filter(
            Q(blood_group__icontains=query)
        )
    paginator = Paginator(users, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context={'page_obj':page_obj}
    return render(request, "myauth/bloodGroup.html",context)



def edit_member(request, instance_id):
    instance = get_object_or_404(User, id=instance_id)
    
    if request.method == 'POST':
        form = MemberForm(request.POST or None, request.FILES or None, instance=instance)
        if form.is_valid():
            form.save()
    form = MemberForm(instance=instance)
    # member=User.objects.get(id=instance_id)
    # if member.fee_amount and member.fee_amount != '0.0':
    #     print('Fees Paid')
    #     today = datetime.now()
    #     member.is_fee_paid=True
    #     member.is_active=True
    #     member.fee_paid_date=timezone.now()
    #     if member.due_date is not None:
    #         due_date=member.due_date
    #         due_date = due_date + relativedelta(months=1)
    #     else:
    #         due_date = today + relativedelta(months=1)
    #     member.due_date=due_date
    #     member.save()
    context = {
        'form': form,
        'instance': instance,
    }
    return render(request, 'myauth/edit_member.html', context)

def revenue_list(request):
    revenue_list = Revenue.objects.all()
    if request.method == 'POST':
        print('POST REQUEST')
        search_revenue_list = []
        query = request.POST.get('query')
        print('query', query)
        users = User.objects.all()
        users = users.filter(
            Q(id__icontains=query) |
            Q(phone__icontains=query) |
            Q(fee_amount__icontains=query) |
            Q(email__icontains=query) |
            Q(username__icontains=query)
        )
        for user in users:
            revenue_list = Revenue.objects.filter(user= user)
            for revenue in revenue_list:
                if not revenue in search_revenue_list:
                    search_revenue_list.append(revenue)
        context = {'revenue_list': search_revenue_list,'query': query}
        return render(request, 'myauth/revenue_list.html', context)
    context = {'revenue_list': revenue_list }
    return render(request, 'myauth/revenue_list.html', context)