from django.db import models
from common.models import User
# Create your models here.

class CallSupport(models.Model):
    reason_type = models.CharField(max_length=255, null=True, blank=True)
    tell_us = models.TextField(blank=True, null=True)
    requested_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE,related_name="request_support")
    requested_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Call Support"
        verbose_name_plural = "Call Supports"

class FeedBack(models.Model):
    price = models.PositiveSmallIntegerField(default=0, null=True, blank=True)
    product = models.PositiveSmallIntegerField(default=0, null=True, blank=True)
    installation = models.PositiveSmallIntegerField(default=0, null=True, blank=True)
    customer_service = models.PositiveSmallIntegerField(default=0, null=True, blank=True)
    review_title = models.CharField(max_length=255, null=True, blank=True)
    user_review = models.TextField(blank=True, null=True)
    feedback_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE,related_name="user_review")

    class Meta:
        verbose_name = "FeedBack"
        verbose_name_plural = "FeedBacks"