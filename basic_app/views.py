from django.shortcuts import render
from basic_app.forms import UserForm, UserProfileInfoForm
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout


def index(request):
    return render(request, 'basic_app/index.html')


# make sure to use the decorators for content where user must be logged in to see the content.
@login_required
def user_logout(request):
    # The django feacher allows me to add easly logout method. This is how we log out user.
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def register(request):
    # Setting as not registered
    registered = False

    # if the req is post, we grab the form
    if request.method == "POST":
        # grab the information of the forms
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        # checking if form is valid
        if user_form.is_valid() and profile_form.is_valid():
            # saving to database
            user = user_form.save()
            # hashing password
            user.set_password(user.password)
            user.save()
            # saving profile
            profile = profile_form.save(commit=False)
            # this code of lane define the One to One relation with User
            profile.user = user

            # this way we deal with any kind of files
            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()
            registered = True

        else:
            print(user_form.errors, profile_form.errors)

    else:
        # not logged in, just settings the form
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    # the userform, profileform, registered we must pass becasue we are using it in the registration.html file as keys!
    return render(request, 'basic_app/registration.html',
                  {'user_form': user_form,
                   'profile_form': profile_form,
                   'registered': registered})


def user_login(request):
    if request.method == 'POST':
        # we get the username, bc this is how we named it in the <input> in login.html template.
        username = request.POST.get('username')
        password = request.POST.get('password')

        # this is django feacher wich will automaticly authenticate the user!
        user = authenticate(username=username, password=password)

        # this is how we log in the user
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))

            else:
                return HttpResponse("Acctount does not exist")
        else:
            print("Someoe tried to login and failed")
            print("Username: {} and password {}".format(username, password))
            return HttpResponse("invalid login details!")

    else:
        # Nothing has been provided for username or password.
        return render(request, 'basic_app/login.html', {})
