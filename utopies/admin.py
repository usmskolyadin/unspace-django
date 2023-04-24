from django.contrib import admin
from .models import Utopies, UtopiaComment



class UtopiesAdmin(admin.ModelAdmin):
    list_display = ('title', 'full_text',)
    prepopulated_fields = {'slug': ('title', )}



class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'utopia', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('author', 'comment')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(active=True)



admin.site.register(Utopies, UtopiesAdmin)
admin.site.register(UtopiaComment)