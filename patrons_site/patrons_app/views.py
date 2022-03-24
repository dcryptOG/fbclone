from django.shortcuts import render
from .forms import UserForm, UserProfileInfoForm

# Extra imports for the lgoin & logout capabilities
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
# Create your views here.

def index(request):
    return render(request,'patrons_app/index.html')

# requires user to be loggedin for view
@login_required
def special(request):
    # set login url in settings.py
    # LOGIN_URL = 'patrons_app/user_login'
    return HttpResponse("You are logged in. Nice!")

@login_required
def user_logout(request):
    # logout the user
    logout(request)
    # REturn to homepage
    return HttpResponseRedirect(reverse('patrons_app/index.html'))

def register(request):
    registered= False
    if request.method=='POST':
        # get info from "both" forms
        # It apprears as one form to the user on the .html page
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        # Check to see both forms are valid
        # is valid from dir(forms.ModelForm)
        if user_form.is_valid() and profile_form.is_valid():

            # Save User Form to Database
            # .save() from dir(forms.ModelForm)
            user = user_form.save()

            # hash the password
            # dir(User) is .set_password
            user.set_password(user.password)

            # update with the hashed password
            user.save()

            # now deal with extra info

            # cant commit yet still need to manipulate
            profile = profile_form.save(commit=False)

            # set ONE to ONE relationship between
            # UserFrom and UserProfileInfoForm

            profile.user = user

            # check if they provided a profile picture
            if 'profile_pic' in request.FILES:
                print('found it')
                # If yes, then grab it from the POST form reply
                profile.profile_pic= request.FILES['profile_pic']

            # now save the model
            profile.save()

            # REgistration Successful
            registered = True

        else:
            # One of the forms was invalid if this else gets called.
            print(user_form.errors, profile_form.errors)

    else:
        # was not an HTTP post so we just render the forms as blank.
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    # This is the render and context dictionary to feed
    # back to the registration.html file page.
    return render(request, 'patrons_app/registration.html',
    {'user_form':user_form,
    'profile_form': profile_form,
    'registered': registered})

def user_login(request):
    if request.method == 'POST':
        # first get the username and assword supplied
        # get name='' from input tag the template login.html
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Django's built-in authentication function:
        user = authenticate(username=username, password=password)

        # If we have a user
        if user:
            # Check if the acount is active
            if user.is_active:
                # log the user in
                login(request,user)
                # send the user back to some page
                # in this case their homepage
                return HttpResponseRedirect(reverse('index'))
            else:
                # if account is not active:
                return HttpResponse("Your account is not active")
        else:
            print("Someone tried to login and failed")
            print(f'They used username: {username} and password: {password}')
            return HttpResponse("Invalid login details supplied")
    else:
        # Nothing has been provided for username or password
        return render(request, 'patrons_app/login.html', {})


