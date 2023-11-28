from django.shortcuts import render,redirect
from .models import creditscore,Profile,Footprint
from django.contrib import messages

# Create your views here.
def profile(request):
    if request.method == 'POST':
        account_number = request.POST['account_number']
        ifsc_code = request.POST['ifsc_code']
        branch_name = request.POST['branch_name']
        age = request.POST['age']
        no_of_degree = request.POST['no_of_degree']
        sex = request.POST['sex']
        is_married = request.POST['is_married']
        dict = {
            'account_number': account_number,
            'ifsc_code': ifsc_code,
            'branch_name': branch_name,
            'age': age,
            'sex': sex,
            'is_married': is_married,
            'No_of_Degrees': no_of_degree,
        }
        user = request.user
        print(user)
        Profile.objects.update_or_create(user_id=user.id, defaults=dict)
        messages.success(request, 'Your Details are saved, now you can proceed')
        return redirect('account')
    else:
        profile = Profile.objects.filter(user=request.user)
        if profile.exists():
            profile = profile[0]
            context = {
                'profile': profile,
            }
        else:
            context = {
                'profile': None,
            }
        print(context)
        return render(request, 'customers/profile.html', context)

def account(request):
    credit_detail = creditscore.objects.filter(profile=request.user.profile)
    if credit_detail.exists():
        credit_detail = credit_detail[0]
        print(credit_detail)
    account_detail = Profile.objects.filter(user=request.user)
    balance = Footprint.objects.filter(profile=request.user.profile)
    if balance.exists():
        balance = balance[0]
    if account_detail.exists():
        account_detail = account_detail[0]
        context = {
            'balance':balance,
            'credit': credit_detail,
            'account': account_detail,
        }
        return render(request,'customers/account.html',context)
    else:
        messages.error(request, 'First Complete Your Profile')
        return redirect('profile')