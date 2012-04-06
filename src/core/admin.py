from django.contrib import admin
from core.models import Speaker, Contact, Talk

class ContactInline(admin.TabularInline):
    model = Contact
    extra = 1

class SpeakerAdmin(admin.ModelAdmin):
    inlines = [ContactInline, ]
    prepopulated_fields = {'slug': ('name',)}
    
class TalkAdmin(admin.ModelAdmin):
    model = Talk
    
admin.site.register(Speaker, SpeakerAdmin)
admin.site.register(Talk, TalkAdmin)