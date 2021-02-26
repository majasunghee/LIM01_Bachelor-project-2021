from django.contrib import admin
from .models import UserAccount
from forstaelse.models import Forstaelse
from chat.models import Chat

# Register your models here.
class AccountAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'is_staff', 'is_active', 'is_superuser')
    search_fields = ('email', 'name')

class ForstaelseAdmin(admin.ModelAdmin):
    list_display = ('chat1', 'question1', 'answer1', 'explanation1', 
                'chat2', 'question2', 'answer2', 'explanation2',
                'chat3', 'question3', 'answer3', 'explanation3')

class ChatAdmin(admin.ModelAdmin):
    list_display = ('chatquestion', 'answer', 'defaultreply', 'userreply')
    
admin.site.register(UserAccount, AccountAdmin)
admin.site.register(Forstaelse, ForstaelseAdmin)
admin.site.register(Chat, ChatAdmin)