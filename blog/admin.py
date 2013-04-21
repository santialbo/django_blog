from blog.models import Entry, Author, Comment, Tag
from django.contrib import admin

admin.site.register(Author)
admin.site.register(Comment)
admin.site.register(Tag)

class EntryAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['author', 'title', 'text', 'date', 'tags']}),
    ]
    list_display = ('title', 'author', 'date')
    list_filter = ['date', 'author__name']
    search_fields = ['title']

admin.site.register(Entry, EntryAdmin)

