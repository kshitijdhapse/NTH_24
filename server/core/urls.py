"""nth_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from .views import *

urlpatterns = [
    # path('users/', UserViewSet.as_view(actions={'get': 'list', 'post': 'create'}), name = 'list-create-users'),
    # path('users/<int:pk>', UserViewSet.as_view(actions={'get': 'retrieve'}), name = 'retrieve-user'),
    # path('questions/<int:level>', QuestionDetail.as_view(), name = 'retrieve-question'), #change URL
    path('userquestion/<slug:user_ans>', QuestionDetail.as_view(), name = 'check_user_ans'), #change URL
    path('leaderboard/', LeaderboardView.as_view(), name = 'leaderboard'),
    path('question/extra-hint/', ExtraHintView.as_view(), name = 'extrahint'),
    path('timer/', TimerView.as_view(), name = 'timer'),
    path('auth/feedback/', FeedbackView.as_view(), name = 'feedback'),
    path('slotmachine/', SlotMachine.as_view(), name = 'slotmachine'),
]
