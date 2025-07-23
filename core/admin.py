from django.contrib import admin
from .models import Note, FlashcardDeck, Flashcard, JournalEntry, TulipVariety

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'created_at')
    list_filter = ('subject', 'created_at')
    search_fields = ('title', 'content')

@admin.register(FlashcardDeck)
class FlashcardDeckAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')

@admin.register(Flashcard)
class FlashcardAdmin(admin.ModelAdmin):
    list_display = ('deck', 'question', 'answer')
    list_filter = ('deck',)

@admin.register(JournalEntry)
class JournalEntryAdmin(admin.ModelAdmin):
    list_display = ('mood', 'created_at')
    list_filter = ('mood', 'created_at')

@admin.register(TulipVariety)
class TulipVarietyAdmin(admin.ModelAdmin):
    list_display = ('name', 'scientific_name', 'color', 'bloom_time')
    list_filter = ('color', 'bloom_time')
    search_fields = ('name', 'scientific_name')