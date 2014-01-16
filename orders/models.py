from django.db import models
from mongoengine import *
from mongoengine.django.auth import User as MongoEngineUser
from django.utils.translation import ugettext_lazy as _

class User(MongoEngineUser):

    #custom fields
    email = EmailField(verbose_name=_('e-mail address'),
                       unique=True)

    
