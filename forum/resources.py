from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget, ManyToManyWidget
from .models import Question, Answer, Follow_section
from accounts.models import CustomUserModel

# --- ১. কোয়েশ্চেন রিসোর্স ---
class QuestionResource(resources.ModelResource):
    author = fields.Field(
        column_name='author_email',
        attribute='author',
        widget=ForeignKeyWidget(CustomUserModel, 'email') # ইমেইল দিয়ে ইউজার আইডি ডিকোড করবে
    )

    class Meta:
        model = Question
        import_id_fields = ('id',)
        fields = ('id', 'author', 'title', 'slug', 'content', 'image', 'created_at')

    def before_import_row(self, row, **kwargs):
        # স্লাগ না থাকলে অটো তৈরি করবে
        if not row.get('slug') and row.get('title'):
            from django.utils.text import slugify
            row['slug'] = slugify(row.get('title'))

# --- ২. অ্যান্সার রিসোর্স ---
class AnswerResource(resources.ModelResource):
    question = fields.Field(
        column_name='question_title',
        attribute='question',
        widget=ForeignKeyWidget(Question, 'title') # প্রশ্নের টাইটেল দেখে উত্তর বসাবে
    )
    author = fields.Field(
        column_name='author_email',
        attribute='author',
        widget=ForeignKeyWidget(CustomUserModel, 'email')
    )

    class Meta:
        model = Answer
        fields = ('id', 'question', 'author', 'content', 'image', 'created_at')

# --- ৩. ফলো সেকশন রিসোর্স ---
class FollowSectionResource(resources.ModelResource):
    user = fields.Field(
        column_name='user_email',
        attribute='user',
        widget=ForeignKeyWidget(CustomUserModel, 'email')
    )
    following = fields.Field(
        column_name='following_emails',
        attribute='following',
        widget=ManyToManyWidget(CustomUserModel, field='email', separator=',') # অনেক ইউজার থাকলে কমা দিয়ে লিখবেন
    )

    class Meta:
        model = Follow_section
        fields = ('id', 'user', 'following', 'created_at')