from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('photobooth/', views.photobooth, name='photobooth'),
    path('tulips/', views.tulips, name='tulips'),
    path('games/', views.games, name='games'),
    path('games/memory/', views.memory_game, name='memory_game'),
    path('games/quiz/', views.quiz_game, name='quiz_game'),
    path('games/puzzle/', views.puzzle_game, name='puzzle_game'),
    path('games/word-search/', views.word_search, name='word_search'),
    path('games/garden-designer/', views.garden_designer, name='garden_designer'),
    path('study/', views.study_companion, name='study_companion'),
    path('notes/', views.notes, name='notes'),
    path('notes/history/', views.notes_history, name='notes_history'),
    path('notes/create/', views.create_note, name='create_note'),
    path('notes/view/<int:note_id>/', views.view_note, name='view_note'),
    path('flashcards/', views.flashcards, name='flashcards'),
    path('clinical-skills/', views.clinical_skills, name='clinical_skills'),
    path('nclex-prep/', views.nclex_prep, name='nclex_prep'),
    path('nursing-curriculum/', views.nursing_curriculum, name='nursing_curriculum'),
    path('download/notes/<str:subject>/', views.download_notes, name='download_notes'),
    path('download/questions/<str:subject>/', views.download_questions, name='download_questions'),

    # ✅ Temporary route to create a Django superuser (remove after use!)
    path('create-admin/', views.create_admin, name='create_admin'),
]
