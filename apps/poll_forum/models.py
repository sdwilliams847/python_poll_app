from __future__ import unicode_literals
from django.db import models
import bcrypt
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9.+_-]+\.[a-zA-Z]+$')
QUES_REGEX = re.compile(r'^[a-zA-Z0-9 .+_ -]+\?$')

class UserManager(models.Manager):
    def register(self, first_name, last_name, email, password, confirm_password):
        
        response = {
            "errors": [],
            "user": None,
            "valid": True
        }
        
        if len(first_name) < 2:
            response["valid"] = False
            response["errors"].append("First name is required")
        if len(last_name) < 2:
            response["valid"] = False
            response["errors"].append("First name is required")
        if len(email) < 1:
            response["valid"] = False
            response["errors"].append("Email address is required")
        elif not EMAIL_REGEX.match(email):
            response["valid"] = False
            response["errors"] = "This email address is invalid"
        else:
            email_list = User.objects.filter(email=email.lower())
            if len(email_list) > 0:
                response["valid"] = False
                response["errors"].append("Email already exists")
        if len(password) < 8:
            response["valid"] = False
            response["errors"].append("Password must be at least 8 characters")
        if confirm_password != password:
            response['valid'] = False
            response["errors"].append("Passwords do not match")
        
        if response['valid']:
            User.objects.create(
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            )
            response['user'] = User.objects.get(email=email.lower())
            
        return response

    def login(self, email, password):
        response = {
            "errors": [],
            "valid": True
        }
        
        if len(email) < 1:
            response["valid"] = False
            response["errors"].append("Email address is required")
        elif not EMAIL_REGEX.match(email):
            response["valid"] = False
            response["errors"].append("The email address you entered is invalid")
        else:
            email_list = User.objects.filter(email=email.lower())
            if len(email_list) == 0:
                response["valid"] = False
                response["errors"].append("Email or password does not match.")
        if len(password) < 8:
            response["valid"] = False
            response["errors"].append("Password must be at least 8 characters")
        if response["valid"]:
            if bcrypt.checkpw(password.encode(), email_list[0].password.encode()):
                response["user"] = email_list[0]
            else:
                response["valid"] = False
                response["errors"].append("Incorrect Password")
        return response

class QuestionManager(models.Manager):
    def newQuestion(self, content, createdBy):
        response = {
            "errors": [],
            "question": None,
            "valid": True
        }

        if len(content) < 10:
            response["valid"] = False
            response["errors"].append("Your question must be at least 10 characters.")
        if not QUES_REGEX.match(content):
            response["valid"] = False
            response["errors"].append("Your question must end with a question mark.")

        if response['valid']:
            response['question']= Question.objects.create(
                content=content,
                createdBy=createdBy,
            )
            
        return response

    def newOption(self, option, relatedQ):
        Option.objects.create(
            option=option,
            relatedQ=relatedQ,
        )

        return

class AnswerManager(models.Manager):
    def newAnswer(self, question, option, answered_by):
        Answer.objects.create(
            question=question,
            option=option,
            answered_by=answered_by,
        )
        print "a new answer was created"
        return




class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
# users field =
    objects = UserManager()

class Question(models.Model):
    content = models.CharField(max_length=1000)
    createdBy =  models.ForeignKey(User, related_name="questions")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
#answers field = all Answers

    objects = QuestionManager()

class Option(models.Model):
    option = models.CharField(max_length=750)
    relatedQ = models.ForeignKey(Question, related_name="options")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    objects = QuestionManager()

class Answer(models.Model):
    question = models.ForeignKey(Question, related_name="answers")
    option = models.ForeignKey(Option, related_name="answers")
    answered_by = models.ForeignKey(User, related_name="answers")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    
    objects = AnswerManager()