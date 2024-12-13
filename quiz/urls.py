from django.urls import path
from . import views

app_name = 'quiz'

urlpatterns = [
    path('', views.home, name='home'), 
    path('start/', views.start_quiz, name='start_quiz'),
    path('question/', views.question, name='question'),
    path('submit/', views.submit_answer, name='submit_answer'),
    path('results/', views.show_results, name='results'),
    path('play-again/', views.play_again, name='play_again'),
    path('exit/', views.exit_game, name='exit_game'),
]
