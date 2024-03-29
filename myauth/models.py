from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from .Manager import CustomUserManager


class User(AbstractUser):
    # username=models.CharField(max_length=50, null=True, blank=True)
    # username=None
    username=models.CharField(max_length=50, null=True, blank=True)
    phone=models.CharField(max_length=50, null=True, blank=True)
    email=models.EmailField(unique=True)
    profile_pic=models.ImageField(null=True, blank=True, default='unknown_profile_pic.jpg')
    blood_group=models.CharField(max_length=10, null=True, blank=True)
    due_date=models.DateField(null=True, blank=True)
    created=models.DateField(auto_now_add=True)
    updated=models.DateField(auto_now=True)
    fee_paid_date=models.DateField(null=True, blank=True)
    fee_amount=models.CharField(max_length=10, null=True, blank=True)
    is_active=models.BooleanField(default=False)
    is_fee_paid=models.BooleanField(default=False)
    is_staff=models.BooleanField(default=False)
    added_by = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='Member_added_by')
    


    USERNAME_FIELD='email'
    REQUIRED_FIELDS=[]
    
    objects = CustomUserManager()

    def __str__(self):
        return str(self.email)
    
class Revenue(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='revenue_user')
    marked_paid_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True, blank=True, related_name='payments_made_by')
    fee_amount = models.DecimalField(max_digits=8, decimal_places=2)
    submission_date = models.DateField(default=timezone.now)
    
    def __str__(self):
        return str(self.user.email)
    def __markedpaid__(self):
        return str(self.marked_paid_by.email)

