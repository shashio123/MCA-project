from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from customers.models import creditscore,Footprint,Profile
from django.contrib import messages
from customers.management.commands.calculate_credit_score import calculate_defaulters_and_creditlimit

# Create your views here.

def manage(request):
    # TODO: check authentication, authorization
    calculate_defaulters_and_creditlimit()
    # get all user profile
    user_profiles = Profile.objects.values('id', 'user__username', 'account_number', 'footprint__updated_at', 'creditscore__potential_defaulter')

    # filter account details from all footprints
    user_profiles_to_edit = list(user_profiles)
    print(user_profiles_to_edit)

    context = {
        'user_profiles': user_profiles_to_edit
    }
    return render(request, 'staff/manage.html', context)

def footprint(request, profileid):
    # TODO: autnethication and authorization

    # get footprint of given profielid
    # prepare context with fields to be edited by manager
    if request.method == 'POST':
        account_balance = request.POST['account_balance']
        pay_0 = request.POST['pay_0']
        pay_1 = request.POST['pay_1']
        pay_2 = request.POST['pay_2']
        pay_3 = request.POST['pay_3']
        pay_4 = request.POST['pay_4']
        pay_5 = request.POST['pay_5']
        bill_amt1 = request.POST['bill_amt1']
        bill_amt2 = request.POST['bill_amt2']
        bill_amt3 = request.POST['bill_amt3']
        bill_amt4 = request.POST['bill_amt4']
        bill_amt5 = request.POST['bill_amt5']
        bill_amt6 = request.POST['bill_amt6']
        pay_amt1 = request.POST['pay_amt1']
        pay_amt2 = request.POST['pay_amt2']
        pay_amt3 = request.POST['pay_amt3']
        pay_amt4 = request.POST['pay_amt4']
        pay_amt5 = request.POST['pay_amt5']
        pay_amt6 = request.POST['pay_amt6']

        print(account_balance)
        diction = {
            'account_balance': account_balance,
            'pay_0': pay_0,
            'pay_1': pay_1,
            'pay_2': pay_2,
            'pay_3': pay_3,
            'pay_4': pay_4,
            'pay_5': pay_5,
            'bill_amt1': bill_amt1,
            'bill_amt2': bill_amt2,
            'bill_amt3': bill_amt3,
            'bill_amt4': bill_amt4,
            'bill_amt5': bill_amt5,
            'bill_amt6': bill_amt6,
            'pay_amt1': pay_amt1,
            'pay_amt2': pay_amt2,
            'pay_amt3': pay_amt3,
            'pay_amt4': pay_amt4,
            'pay_amt5': pay_amt5,
            'pay_amt6': pay_amt6,
        }
        Footprint.objects.update_or_create(profile_id=profileid, defaults=diction)
        messages.success(request, 'Customers Details are saved, now you can proceed')
        return redirect('manage')


    footprints = Footprint.objects.filter(profile_id=profileid)
    if footprints.exists():
            footprints = footprints[0]
            context = {
                'footprints': footprints,
                'profileid': profileid,
            }
            return render(request, 'staff/footprint.html', context)

