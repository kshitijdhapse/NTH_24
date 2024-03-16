from django.contrib import admin
from .models import *

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'current_level', 'hidden_on_leaderboard')
    readonly_fields=('last_level_updated_time',)
    fieldsets = (
        (None, {
            "fields": (
                ('username', 'current_level'), ('first_name', 'last_name'), ('email','phone', 'hidden_on_leaderboard'), ('paidHintTaken', 'keys'), ('is_active', 'promo_used'),('is_superuser','is_staff'),('is_rigged','machine_used'),
                'last_level_updated_time',
            ),
        }),
    )
    
class HistoryAdmin(admin.ModelAdmin):
    list_display = ( 'user', 'question', 'last_updated') # specify the fields to display in the table
    list_filter = ('last_updated', 'question', 'user') # specify filters to display on the right-hand side of the table
    search_fields = ('user__username', 'question__title') # specify fields to search on using the search box

admin.site.register(User, UserAdmin)
admin.site.register(Question)
admin.site.register(Feedback)
admin.site.register(Timer)
admin.site.register(AnswerHistory, HistoryAdmin)
