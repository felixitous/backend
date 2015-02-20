from django.db import models
import datetime
import StringIO
import logging
from django.db import IntegrityError

class User(models.Model):
    user = models.CharField(unique=True, max_length=128)
    first_name = models.CharField(max_length=128, null=True)
    last_name = models.CharField(max_length=128, null=True)
    teacher = models.CharField(max_length=128, null=True)
    school = models.CharField(max_length=128, null=True)
    period = models.IntegerField(null=True)
    email = models.CharField(max_length=128, unique=True, null=True)


    def login(self, username):
        try:
            selected_choice = UsersModel.objects.get(user=username)
        except UsersModel.DoesNotExist:
            errcode = -1
            return [None,errcode,None,None]
        else:
            errcode=1
            return [selected_choice.user,errcode,selected_choice.teacher,selected_choice.period]

    #WARNING: We can take out this method. It can be deprecated
    def get_user_id(self,username):
        try:
            selected_choice = UsersModel.objects.get(user=username)
        except:
            errcode = -1
            return [None,errcode]
        else:
            errcode=1
            return[selected_choice.user,errcode]

    def add_user(self, username, school, teacher, period, first_name, last_name, email):
        try:
            selected_choice = UsersModel.objects.get(user=username)
        except UsersModel.DoesNotExist:
            newuser = UsersModel()
            newuser.user=username
            newuser.teacher = teacher
            newuser.school = school
            newuser.period = period
            newuser.user_id = len(UsersModel.objects.all())
            newuser.first_name = first_name
            newuser.last_name = last_name
            newuser.email = email
            newuser.save()
            errcode = 1
            return [errcode,0]
        else:
            #that user is already there
            errcode = -1
            return [errcode,0]

    def get_classmates(self, t, p):
        try:
            selected_choice = UsersModel.objects.filter(teacher=t).filter(period=p)
        except UsersModel.DoesNotExist:
            return [None,None,None,-1]
        #WE NEED TO WAIT FOR THE QUERY TO RETURN!
        else:
            first_names=[]
            last_names=[]
            user_ids = []
            for x in selected_choice:
                first_names.append(x.first_name)
                last_names.append(x.last_name)
                user_ids.append(x.user)
            return [first_names,last_names,user_ids,1]

class InvitesModel(models.Model):
    user = models.CharField(max_length=128, null=True)
    invite_id = models.IntegerField(unique=True, null=True)
    handout = models.ForeignKey('HandoutModel')

    """
    This needs to be updated
    class Meta:
        unique_together = ("user_id", "handout")
    """

    def put_invite(self, u,h):
        newinvite = InvitesModel()
        newinvite.user = u
        newinvite.invite_id = len(InvitesModel.objects.all())
        newinvite.handout = h
        try:
            newinvite.save()
            return 1
        except IntegrityError:
            return -1

    #returns -1 if there are no items found, and 1 if items are found
    def get_invite(self,u,t,p):
        try:
            selected_choice = InvitesModel.objects.filter(user=u)
        except InvitesModel.DoesNotExist:
            return [None,None,-1]
        else:
            file_names=[]
            dates=[]
            for x in selected_choice:
                x=x.handout
                if (x.teacher==t and x.period==int(p)):
                    file_names.append(x.file_name)
                    dates.append(str(x.date.date()))
            return [file_names,dates,1]



class HandoutModel(models.Model):
    #We aren't having teachers push out the files itself, once that happens we will use a File ID
    handout_id = models.IntegerField(unique=True, null=True)
    teacher = models.CharField(max_length=128,  null=True)
    period = models.IntegerField(null=True)
    #this is the name of the file in Google Drive
    file_name = models.CharField(max_length=128,  null=True)
    date = models.DateTimeField(null=True)

    """
    @returns a list of handout objects (up to 3)
    if there are no handouts, it will return a handout List with 1 item [None]
    """
    def get_handouts(self, teacher, period):
        try:
            selected_choice = HandoutModel.objects.filter(teacher=teacher,period=period).order_by('date')
        except HandoutModel.DoesNotExist:
            return [None]
        else:
            result = []
            i = 0
            for x in selected_choice:
                result.append(x.file_name)
                i+=1
                if i==3:
                    break
            return result

    def put_handout(self, t, p, f):
        try:
            selected_choice = HandoutModel.objects.get(file_name=f)
        except HandoutModel.DoesNotExist:
            newhand = HandoutModel()
            newhand.handout_id=len(HandoutModel.objects.all())
            newhand.teacher = t
            newhand.period = p
            newhand.file_name = f
            newhand.date = datetime.datetime.now()
            newhand.save()
            errcode = 1
            return errcode
        else:
            #that handout is already there
            errcode = -1
            return errcode

    def get_handout_from_file_name(self, f):
        try:
            selected_choice = HandoutModel.objects.get(file_name=f)
        except HandoutModel.DoesNotExist:
            return None
        else:
            return selected_choice
