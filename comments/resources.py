from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from .models import Comment, Reply
from blog_post.models import BlogPost
from accounts.models import CustomUserModel

class CommentResource(resources.ModelResource):
    post = fields.Field(
        column_name='blog_post_title',
        attribute='post',
        widget=ForeignKeyWidget(BlogPost, 'title') 
    )
    user = fields.Field(
        column_name='user_email',
        attribute='user',
        widget=ForeignKeyWidget(CustomUserModel, 'email') 
    )

    class Meta:
        model = Comment
        import_id_fields = ('id',)
        fields = ('id', 'post', 'user', 'content', 'created_at')

class ReplyResource(resources.ModelResource):
    comment = fields.Field(
        column_name='parent_comment_id',
        attribute='comment',
        widget=ForeignKeyWidget(Comment, 'id')
    )
    user = fields.Field(
        column_name='user_email',
        attribute='user',
        widget=ForeignKeyWidget(CustomUserModel, 'email')
    )

    class Meta:
        model = Reply
        import_id_fields = ('id',)
        fields = ('id', 'comment', 'user', 'content', 'created_at')