from django.db import models

from users.models import User


class Order(models.Model):
    """
        docstring
    """
    CASH = "CA"
    CREDIT = "CR"
    PAYMENT = [
        ("CA", "Cash"),
        ("CR", "Credit"),
    ]

    client = models.ForeignKey(User, on_delete=models.CASCADE)
    # expert = models.ForeignKey(Expert, on_delete=models.CASCADE)
    # service = models.ForeignKey(Service, on_delete=models.CASCADE)
    client_score = models.IntegerField(default=0)
    expert_score = models.IntegerField(default=0)
    description = models.TextField(max_length=1024)
    order_price = models.IntegerField(default=0)
    is_arrived = models.BooleanField(default=False)
    status = models.IntegerField(default=0)

    comission = models.IntegerField(default=0)
    tax = models.IntegerField(default=0)

    address = models.TextField(max_length=1024)
    payment = models.CharField(max_length=2, choices=PAYMENT, default=CREDIT)
    register_time = models.DateTimeField(auto_now_add=True)
    finish_time = models.DateTimeField(auto_now_add=True)
