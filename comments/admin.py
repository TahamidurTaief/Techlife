from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline
from unfold.contrib.import_export.forms import ExportForm, ImportForm
from import_export.admin import ImportExportModelAdmin
from .models import Comment, Reply
from .resources import CommentResource, ReplyResource

class ReplyInline(TabularInline):
    model = Reply
    extra = 1
    fields = ('user', 'content', 'created_at')
    readonly_fields = ('created_at',)

@admin.register(Comment)
class CommentAdmin(ModelAdmin, ImportExportModelAdmin):
    resource_class = CommentResource
    import_form_class = ImportForm
    export_form_class = ExportForm

    list_display = ('user', 'post_title_short', 'content_preview', 'created_at')
    list_filter = ('created_at', 'post')
    search_fields = ('content', 'user__email', 'post__title')
    inlines = [ReplyInline]

    def post_title_short(self, obj):
        return obj.post.title[:30] + "..." if len(obj.post.title) > 30 else obj.post.title
    post_title_short.short_description = "Post"

    def content_preview(self, obj):
        return obj.content[:50] + "..." if len(obj.content) > 50 else obj.content
    content_preview.short_description = "Comment Content"

@admin.register(Reply)
class ReplyAdmin(ModelAdmin, ImportExportModelAdmin):
    resource_class = ReplyResource
    import_form_class = ImportForm
    export_form_class = ExportForm

    list_display = ('user', 'parent_comment_preview', 'created_at')
    search_fields = ('content', 'user__email', 'comment__content')
    list_filter = ('created_at',)

    def parent_comment_preview(self, obj):
        return obj.comment.content[:40] + "..." if len(obj.comment.content) > 40 else obj.comment.content
    parent_comment_preview.short_description = "Replying To"