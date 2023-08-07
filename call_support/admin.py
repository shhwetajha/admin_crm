# from django.contrib import admin
# from .models import FeedBack, CallSupport
# # Register your models here.

# class FeedBackAdmin(admin.ModelAdmin):
    
#     list_display = ["feedback_by", "review_title",  "price", "product", "installation", "customer_service", "user_review"]
#     list_filter = ('feedback_by',)
#     search_fields = ('feedback_by__email',)

# class CallSupportAdmin(admin.ModelAdmin):
    
#     list_display = ["requested_by",  "reason_type", "tell_us", "requested_at"]
#     list_filter = ('requested_by',)
#     search_fields = ('requested_by__email',)

# admin.site.register(FeedBack, FeedBackAdmin)
# admin.site.register(CallSupport, CallSupportAdmin)