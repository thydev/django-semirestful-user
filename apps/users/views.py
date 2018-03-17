from django.shortcuts import render, redirect
from .models import User
from django.contrib import messages

# 1 - Display all the users
def index(request):
    context = {
        'users': User.objects.all()
    }
    return render(request, "users/index.html", context)

# 2 - Display the form for user to input the data
def new(request):
    
    return render(request, "users/new.html")

# 3 - Show the editing user data on the form
def edit(request, id):
    context = {
        'user': User.objects.get(id = id),
    }
    return render(request, "users/edit.html", context)

# 4 - Show user's information
def show(request, id):
    context = {
        'user': User.objects.get(id=id),
    }
    return render(request, "users/show.html", context)

# 5 Post route to insert the data into the database
def create(request):
    # Validation for creating new user
    errors = User.objects.create_validator(request.POST)
    if len(errors) > 0:
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/users/new')

    # Assign the saved user to newuser
    newuser = User.objects.create(first_name = request.POST['first_name'], last_name = request.POST['last_name'], email = request.POST['email'])
    
    # redirect to the display route
    return redirect("/users/{}".format(newuser.id))

# 6 - Delete user from the database
def destroy(request, id):
    User.objects.get(id=id).delete()
    return redirect("/users")

# 7 - Save changes
def update(request):
    if request.method != "POST":
        return redirect('/')
    # Validation for editing user
    errors = User.objects.update_validator(request.POST)
    if len(errors) > 0:
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/users/{}/edit'.format(request.POST['user_id']))

    updated_user = User.objects.get(id=request.POST['user_id'])
    updated_user.first_name = request.POST['first_name']
    updated_user.last_name = request.POST['last_name']
    updated_user.email = request.POST['email']
    updated_user.save()
    
    return redirect("/users/{}".format(updated_user.id))
