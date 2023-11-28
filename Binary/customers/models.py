from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING)
    account_number = models.IntegerField()
    ifsc_code = models.CharField(max_length=200)
    branch_name = models.CharField(max_length=100)
    age = models.IntegerField()
    sex = models.IntegerField()
    is_married = models.BooleanField(default=False)
    No_of_Degrees = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args , **kwargs):
        # TODO: change footprint_updated only for certain fields
        super(Profile, self).save(*args, **kwargs)
        creditscore.objects.update_or_create(profile=self, defaults={'footprint_updated': True})

pay_choices = {
    (-1, 'Paid before time'),
    (0, 'Paid on time'),
    (1, 'Paid after 1 month'),
    (2, 'Paid after 2 month'),
    (3, 'Paid after 3 month'),
    (4, 'Paid after 4 month'),
    (5, 'Paid after 5 month'),
    (6, 'Paid after 6 month'),
    (7, 'Paid after 7 month'),
    (8, 'Paid after 8 month')
}
class Footprint(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.DO_NOTHING)
    account_balance = models.IntegerField()
    pay_0 = models.IntegerField(default=-1, help_text='1st Loan status', choices=pay_choices)
    pay_1 = models.IntegerField(default=-1, help_text='2nd Loan status', choices=pay_choices)
    pay_2 = models.IntegerField(default=-1, help_text='2nd Loan status', choices=pay_choices)
    pay_3 = models.IntegerField(default=-1, help_text='2nd Loan status', choices=pay_choices)
    pay_4 = models.IntegerField(default=-1, help_text='2nd Loan status', choices=pay_choices)
    pay_5 = models.IntegerField(default=-1, help_text='2nd Loan status', choices=pay_choices)
    bill_amt1 = models.IntegerField(default=0, help_text='1st Loan amount')
    bill_amt2 = models.IntegerField(default=0)
    bill_amt3 = models.IntegerField(default=0)
    bill_amt4 = models.IntegerField(default=0)
    bill_amt5 = models.IntegerField(default=0)
    bill_amt6 = models.IntegerField(default=0)
    pay_amt1 = models.IntegerField(default=0)
    pay_amt2 = models.IntegerField(default=0)
    pay_amt3 = models.IntegerField(default=0)
    pay_amt4 = models.IntegerField(default=0)
    pay_amt5 = models.IntegerField(default=0)
    pay_amt6 = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args , **kwargs):
        creditscore.objects.update_or_create(profile=self.profile, defaults={'footprint_updated': True})
        super(Footprint, self).save(*args, **kwargs)







class creditscore(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.DO_NOTHING)
    score = models.IntegerField(default=500)
    potential_defaulter = models.BooleanField(default=True)
    footprint_updated = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
