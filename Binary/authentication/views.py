from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages,auth
from django.contrib.auth.models import Group


# Create your views here.
def register(request):
    if request.method == 'POST':
        # get form values
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']



        if request.POST['groupName']:
            my_group_name = request.POST['groupName']
            # Check matching password
            if password == password2:
                # check username
                if User.objects.filter(username=username).exists():
                    messages.error(request, 'Username not available')
                    return redirect('register')
                else:
                    if User.objects.filter(email=email).exists():
                        messages.error(request, 'That email is in use')
                        return redirect('register')
                    else:
                        if Group.objects.filter(name=my_group_name).exists():
                            # looks good
                            user = User.objects.create_user(username=username, password=password, email=email,
                                                            first_name=first_name, last_name=last_name)
                            # login after register
                            # auth.login(request,user)
                            # messages.success(request,'You are now registered')
                            # return redirect('index')
                            user.save();
                            my_group = Group.objects.get(name=my_group_name)
                            data=Group.objects.all()
                            print(data)
                            print('Group',my_group_name)
                            my_group.user_set.add(user)
                            messages.success(request, 'You are now registered proceed to login')
                            return redirect('login')
                        else:
                            messages.error(request, 'Group not exists')
                            return redirect('register')
            else:
                messages.error(request, 'Password do not match')
                return redirect('register')
        else:
            messages.error(request, 'No group selected')
            return redirect('register')
    else:
        return render(request, 'authentication/register.html')



def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password= password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are now logged in')
            return redirect('index')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('login')
    else:
        return render(request, 'authentication/login.html')


def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, 'You are logged out')
        return redirect('index')