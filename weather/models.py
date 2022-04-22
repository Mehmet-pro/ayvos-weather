from django.db import models
from django.contrib.auth.models import User

class Cities(models.Model):
    city = models.CharField(max_length=20)

    def __str__(self):
        return self.city


class Logs(models.Model):
    user_id = models.ForeignKey(User,blank=False,null=False,on_delete=models.CASCADE)
    log_date = models.DateTimeField(auto_now_add=True)
    location_id = models.ForeignKey(Cities,blank=True,null=True,on_delete=models.CASCADE)
    ip_address = models.CharField(max_length=14,blank=False,null=False)
    resault = models.CharField(max_length=100,blank=False,null=False)
    response_time = models.IntegerField(blank=False,null=False)
    response_state = models.BooleanField(blank=False,null=False,default=False)
