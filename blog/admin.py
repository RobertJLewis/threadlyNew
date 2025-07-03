from django.contrib import admin
from .models import Category, Thread, Comment, ThreadReaction, Slide

@admin.register(Slide)
class SlideAdmin(admin.ModelAdmin):
    list_display = ("title", "timestamp", "summary")


admin.site.register(Category)
admin.site.register(Thread)
admin.site.register(Comment)
admin.site.register(ThreadReaction)