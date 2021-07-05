
from django.urls import path
from . import views as wall_views
from notifications import views as notification_views


urlpatterns = [
    path('', wall_views.home, name="home"),
    path('mostpopular/', wall_views.most_popular, name="popular"),
    path('profile/<str:username>/', wall_views.profile, name="Profile"),
    path('like/<int:like>/', wall_views.like_post, name="Like"),
    path('post/<int:post_id>/', wall_views.single_post, name="Single_Post"),
    path('post/new/', wall_views.new_post, name="New_Post"),
    path('post/<int:post_id>/next', wall_views.next_new_post, name="Next_New_Post"),
    path('post/<int:post_id>/edit', wall_views.edit_post, name="Edit_Post"),
    path('post/<int:post_id>/delete', wall_views.delete_post, name="Delete_Post"),
    path('comment/<int:post_id>', wall_views.new_comment, name="Comment"),
    path('reply/<int:post_id>', wall_views.reply_comment, name="Reply"),
    path('comment/<int:comment_id>/like', wall_views.like_comment, name="Like_Comment"),
    path('comment/<int:comment_id>/unlike', wall_views.unlike_comment, name="Unlike_Comment"),
    path('comment/<int:post_id>', wall_views.new_comment, name="Comment"),
    path('comment/<int:comment_id>/delete', wall_views.delete_comment, name="Delete_comment"),
    path('reply/<int:reply_id>/delete', wall_views.delete_reply, name="Delete_reply"),
    path('notification/read', notification_views.notification_read, name="Notification_read"),
]
