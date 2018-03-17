from __future__ import unicode_literals
from django.db import models
from django.db.models import Q
# Create your models here.

# No methods in our new manager should ever catch the whole request object with a parameter!!! 
# (just parts, like request.POST)
class UserManager(models.Manager):
    def create_validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 2:
            errors["first_name"] = "First name should be more than 2 characters"
        if len(postData['last_name']) < 2:
            errors["last_name"] = "Last name should be more than 2 characters"
        if len(postData["email"]) < 2:
            errors['email'] = "Invalid email address"
        elif User.objects.filter(email=postData['email']).count() > 0:
            errors['email'] = "This email {} is already exist".format(postData['email'])

        return errors

    def update_validator(self, postData):
        errors = {}
        
        if len(postData['first_name']) < 2:
            errors["first_name"] = "First name should be more than 2 characters"
        if len(postData['last_name']) < 2:
            errors["last_name"] = "Last name should be more than 2 characters"
        if len(postData["email"]) < 2:
            errors['email'] = "Invalid email address"
        # Check the email if it already exists and do not count its self
        # print "user filter", User.objects.exclude(id = postData['user_id']).filter(email = postData['email']).count()
        # print User.objects.filter(~Q(id = postData['user_id']) & Q(email = postData['email'])).count()
        elif User.objects.filter(~Q(id = postData['user_id']) & Q(email = postData['email'])).count() > 0:
            errors['email'] = "This email {} already exists".format(postData['email'])

        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=254)
    email = models.CharField(max_length=254)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Connect an instance of UserManager to our User model overwriting
    # the old hidden objects key with a new one with extra properties !
    objects = UserManager()

    def __repr__(self):
        return "<User Object: first_name: {}, last_name: {}>".format(self.first_name, self.last_name)