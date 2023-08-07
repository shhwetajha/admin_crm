from django.apps import AppConfig
from django.db.models.signals import post_save
print("""               
    ______     ______  ______  ___  ___   ___
    | | \ \    | |__|  | |  /  | |  | |\  | |
    | |__\ \   | |__   | |_/   | |  | | \ | |
    |_|   \_\  |_|     |_| \   |_|  |_|  \|_|
    -----------------------------------------
    """)
class CommonConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'common'
    def ready(self):
        from order.models import Order
        from common.models import User
        from common.signals.handlers import update_user_type, update_order_id
        post_save.connect(update_user_type, sender=User, dispatch_uid='update_user_type')
        post_save.connect(update_order_id, sender=Order, dispatch_uid='update_order_id')