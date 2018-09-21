from django.contrib import admin
from .models import user,post,history,review

# Register your models here.
class userAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'time_created']
admin.site.register(user, userAdmin)

class postAdmin(admin.ModelAdmin):
    list_display = ['id', 'name','poster','time_created','visible','active']
admin.site.register(post, postAdmin)

class historyAdmin(admin.ModelAdmin):
    list_display = ['id', 'post', 'student', 'time_created']
admin.site.register(history, historyAdmin)

class reviewAdmin(admin.ModelAdmin):
    list_display = ['id', 'history', 'rate', 'time_created']
admin.site.register(review, reviewAdmin)
