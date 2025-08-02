from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Count
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import (
    Note, FlashcardDeck, Flashcard, JournalEntry, TulipVariety, 
    ClinicalSkill, StudyPlan, StudyPlanSubject, NCLEXQuestion, StudySession
)

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'user', 'priority', 'word_count', 'is_public', 'created_at', 'updated_at')
    list_filter = ('subject', 'priority', 'is_public', 'created_at', 'user')
    search_fields = ('title', 'content', 'tags')
    readonly_fields = ('created_at', 'updated_at', 'word_count')
    list_editable = ('priority', 'is_public')
    list_per_page = 25
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'subject', 'user')
        }),
        ('Content', {
            'fields': ('content', 'tags')
        }),
        ('Settings', {
            'fields': ('priority', 'is_public')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at', 'word_count'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')
    
    def save_model(self, request, obj, form, change):
        if not change and not obj.user:
            obj.user = request.user
        super().save_model(request, obj, form, change)

class FlashcardInline(admin.TabularInline):
    model = Flashcard
    extra = 1
    fields = ('question', 'answer', 'difficulty', 'order')
    ordering = ('order',)

@admin.register(FlashcardDeck)
class FlashcardDeckAdmin(admin.ModelAdmin):
    list_display = ('name', 'subject', 'user', 'card_count', 'is_public', 'created_at')
    list_filter = ('subject', 'is_public', 'created_at', 'user')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at', 'card_count')
    inlines = [FlashcardInline]
    list_per_page = 20
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'subject', 'user')
        }),
        ('Settings', {
            'fields': ('is_public',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at', 'card_count'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not change and not obj.user:
            obj.user = request.user
        super().save_model(request, obj, form, change)

@admin.register(Flashcard)
class FlashcardAdmin(admin.ModelAdmin):
    list_display = ('deck', 'question_preview', 'difficulty', 'order', 'created_at')
    list_filter = ('difficulty', 'deck__subject', 'created_at')
    search_fields = ('question', 'answer', 'hint')
    list_editable = ('difficulty', 'order')
    readonly_fields = ('created_at',)
    
    def question_preview(self, obj):
        return obj.question[:50] + "..." if len(obj.question) > 50 else obj.question
    question_preview.short_description = "Question"

@admin.register(JournalEntry)
class JournalEntryAdmin(admin.ModelAdmin):
    list_display = ('title_or_date', 'user', 'mood_display', 'word_count', 'is_private', 'created_at')
    list_filter = ('mood', 'is_private', 'created_at', 'user')
    search_fields = ('title', 'content', 'tags')
    readonly_fields = ('created_at', 'updated_at', 'word_count')
    list_per_page = 25
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Entry Details', {
            'fields': ('title', 'content', 'user')
        }),
        ('Mood & Tags', {
            'fields': ('mood', 'tags')
        }),
        ('Privacy', {
            'fields': ('is_private',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at', 'word_count'),
            'classes': ('collapse',)
        }),
    )
    
    def title_or_date(self, obj):
        return obj.title if obj.title else f"Entry - {obj.created_at.strftime('%Y-%m-%d')}"
    title_or_date.short_description = "Title/Date"
    
    def mood_display(self, obj):
        mood_colors = {
            'happy': '#10B981',
            'content': '#3B82F6', 
            'neutral': '#6B7280',
            'sad': '#F59E0B',
            'stressed': '#EF4444',
            'excited': '#8B5CF6',
            'tired': '#6B7280',
            'anxious': '#F59E0B',
            'grateful': '#10B981',
            'motivated': '#8B5CF6',
        }
        color = mood_colors.get(obj.mood, '#6B7280')
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            obj.get_mood_display()
        )
    mood_display.short_description = "Mood"

@admin.register(StudySession)
class StudySessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'subject', 'session_type', 'duration_minutes', 'productivity_rating', 'created_at')
    list_filter = ('subject', 'session_type', 'productivity_rating', 'created_at', 'user')
    search_fields = ('notes_text', 'user__username')
    readonly_fields = ('created_at',)
    filter_horizontal = ('notes_reviewed', 'flashcard_decks_used')
    list_per_page = 25
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Session Details', {
            'fields': ('user', 'subject', 'session_type', 'duration_minutes')
        }),
        ('Content Reviewed', {
            'fields': ('notes_reviewed', 'flashcard_decks_used')
        }),
        ('Reflection', {
            'fields': ('productivity_rating', 'notes_text')
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

@admin.register(TulipVariety)
class TulipVarietyAdmin(admin.ModelAdmin):
    list_display = ('name', 'scientific_name', 'color', 'bloom_time', 'height', 'created_at')
    list_filter = ('color', 'bloom_time', 'created_at')
    search_fields = ('name', 'scientific_name', 'description')
    readonly_fields = ('created_at', 'updated_at')
    list_per_page = 20
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'scientific_name', 'description')
        }),
        ('Characteristics', {
            'fields': ('color', 'bloom_time', 'height')
        }),
        ('Care & Media', {
            'fields': ('care_instructions', 'image_url')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(ClinicalSkill)
class ClinicalSkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'competency_level', 'created_at')
    list_filter = ('category', 'competency_level', 'created_at')
    search_fields = ('name', 'description', 'steps')
    readonly_fields = ('created_at', 'updated_at')
    list_per_page = 20
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'category', 'competency_level')
        }),
        ('Content', {
            'fields': ('description', 'steps', 'safety_considerations', 'equipment_needed')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

class StudyPlanSubjectInline(admin.TabularInline):
    model = StudyPlanSubject
    extra = 1
    fields = ('subject', 'priority', 'target_hours', 'completed_hours')

@admin.register(StudyPlan)
class StudyPlanAdmin(admin.ModelAdmin):
    list_display = ('user', 'semester', 'year', 'created_at')
    list_filter = ('semester', 'year', 'created_at', 'user')
    search_fields = ('user__username', 'semester')
    readonly_fields = ('created_at',)
    inlines = [StudyPlanSubjectInline]
    
    def save_model(self, request, obj, form, change):
        if not change and not obj.user:
            obj.user = request.user
        super().save_model(request, obj, form, change)

@admin.register(NCLEXQuestion)
class NCLEXQuestionAdmin(admin.ModelAdmin):
    list_display = ('question_preview', 'question_type', 'category', 'difficulty', 'created_at')
    list_filter = ('question_type', 'category', 'difficulty', 'created_at')
    search_fields = ('question_text', 'rationale', 'category')
    readonly_fields = ('created_at', 'updated_at')
    list_per_page = 20
    
    fieldsets = (
        ('Question Details', {
            'fields': ('question_text', 'question_type', 'category', 'difficulty')
        }),
        ('Answer Options', {
            'fields': ('options', 'correct_answers')
        }),
        ('Explanation', {
            'fields': ('rationale',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def question_preview(self, obj):
        return obj.question_text[:75] + "..." if len(obj.question_text) > 75 else obj.question_text
    question_preview.short_description = "Question"

# Customize admin site
admin.site.site_header = "Bloom Study Platform Admin"
admin.site.site_title = "Bloom Admin"
admin.site.index_title = "Welcome to Bloom Administration"