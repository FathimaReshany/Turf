from django.contrib import admin
from turfapp import models




class SlotAdmin(admin.ModelAdmin):
    list_display = ('slot_name' ,'time' , 'end_time')
    list_editable = ('time' , 'end_time')

class BookingAdmin(admin.ModelAdmin):
    list_display = ('date' ,'user' , 'offer_applied', 'slot', 'total_amount')
    sortable_by = ('date',)

class Userdetail_Admin(admin.ModelAdmin):
    list_display = ('name' ,'user' , 'mobile', 'mailid', 'ref_code')
    sortable_by = ('name',)

class Feedback_Admin(admin.ModelAdmin):
    list_display = ('username', 'feedback')
    sortable_by = ('username',)







# Register your models here.
admin.site.register(models.Offer)
admin.site.register(models.Slot , SlotAdmin)
# admin.site.register(models.Transaction)
# admin.site.register(models.Coin)
# admin.site.register(models.Coinsref)
admin.site.register(models.UserDetail , Userdetail_Admin)
admin.site.register(models.Gallery)
admin.site.register(models.Settings)
admin.site.register(models.Referrals)
admin.site.register(models.Booking , BookingAdmin)
admin.site.register(models.Feedback , Feedback_Admin)


