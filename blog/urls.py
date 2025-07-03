from django.urls import path
from . import views

urlpatterns = [
    path("category/<slug:slug>/", views.CategoryThreadList.as_view(), name="category_feed"),
    path("thread/new/<slug:cat_slug>/", views.ThreadCreate.as_view(), name="thread_create"),
    path("thread/<int:pk>/",           views.ThreadDetail.as_view(), name="thread_detail"),
    path("thread/<int:pk>/react/",     views.react_to_thread,    name="thread_react"),
    path("thread/<int:pk>/comment/",   views.comment_on_thread,  name="thread_comment"),
]
