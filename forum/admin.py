from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline
from unfold.contrib.import_export.forms import ExportForm, ImportForm
from import_export.admin import ImportExportModelAdmin
from .models import Question, Answer, Follow_section
from .resources import QuestionResource, AnswerResource, FollowSectionResource

# --- Inline for Answers within Question ---
class AnswerInline(TabularInline): # Unfold TabularInline ব্যবহার করা হয়েছে
    model = Answer
    extra = 1
    fields = ('author', 'content', 'created_at')
    readonly_fields = ('created_at',)

# --- Question Admin ---
@admin.register(Question)
class QuestionAdmin(ModelAdmin, ImportExportModelAdmin):
    resource_class = QuestionResource
    import_form_class = ImportForm
    export_form_class = ExportForm
    
    list_display = ('title', 'author', 'created_at')
    search_fields = ('title', 'content', 'author__email', 'author__first_name')
    list_filter = ('created_at', 'author')
    readonly_fields = ('created_at',)
    inlines = [AnswerInline]
    prepopulated_fields = {'slug': ('title',)}

# --- Answer Admin ---
@admin.register(Answer)
class AnswerAdmin(ModelAdmin, ImportExportModelAdmin):
    resource_class = AnswerResource
    import_form_class = ImportForm
    export_form_class = ExportForm
    
    list_display = ('question_short', 'author', 'created_at')
    search_fields = ('content', 'author__email', 'question__title')
    list_filter = ('created_at', 'author')
    
    def question_short(self, obj):
        return obj.question.title[:50]
    question_short.short_description = "Question Title"

# --- Follow Section Admin ---
@admin.register(Follow_section)
class FollowSectionAdmin(ModelAdmin, ImportExportModelAdmin):
    resource_class = FollowSectionResource
    import_form_class = ImportForm
    export_form_class = ExportForm
    
    list_display = ('user', 'followers_count_display', 'following_count_display')
    
    def followers_count_display(self, obj):
        return obj.followers_count()
    followers_count_display.short_description = "Followers"

    def following_count_display(self, obj):
        return obj.following_count()
    following_count_display.short_description = "Following"