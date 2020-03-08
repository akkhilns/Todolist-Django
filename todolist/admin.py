from django.contrib import admin
# the module name is app_name.models
from todolist.models import Post
# this class define which department columns will be shown in the department admin web site.
class TodoListAdmin(admin.ModelAdmin):
    # a list of displayed columns name.
    list_display = ['id', 'author','title', 'text']
admin.site.register(Post, TodoListAdmin)