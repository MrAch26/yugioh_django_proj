from django.urls import path
from . import views

urlpatterns = [
    path('', views.ForumView.as_view(), name='forum'),
    path('add/', views.ForumCreate.as_view(), name='forum-add'),  # need to be before slug
    path('edit/<int:pk>', views.ForumUpdateView.as_view(), name='forum-edit'),
    path('by/<username>/', views.ForumUserListView.as_view(), name='forum-user'),
    path('<slug:slug>/', views.ForumDetailView.as_view(), name='forum-detail')
]
