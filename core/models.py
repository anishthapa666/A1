from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Note(models.Model):
    SUBJECT_CHOICES = [
        ('fundamentals', 'Fundamentals of Nursing'),
        ('anatomy_physiology', 'Anatomy & Physiology'),
        ('pharmacology', 'Pharmacology'),
        ('pathophysiology', 'Pathophysiology'),
        ('medical_surgical', 'Medical-Surgical Nursing'),
        ('pediatric', 'Pediatric Nursing'),
        ('maternity', 'Maternity & Women\'s Health'),
        ('mental_health', 'Mental Health Nursing'),
        ('community_health', 'Community Health Nursing'),
        ('critical_care', 'Critical Care Nursing'),
        ('nursing_ethics', 'Nursing Ethics & Law'),
        ('research', 'Nursing Research'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    subject = models.CharField(max_length=50, choices=SUBJECT_CHOICES)
    title = models.CharField(max_length=200)
    content = models.TextField()
    tags = models.CharField(max_length=500, blank=True, help_text="Comma-separated tags")
    is_public = models.BooleanField(default=False, help_text="Make this note visible to other users")
    priority = models.CharField(max_length=20, choices=[
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ], default='medium')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at', '-created_at']
        indexes = [
            models.Index(fields=['subject']),
            models.Index(fields=['created_at']),
            models.Index(fields=['user']),
        ]

    def __str__(self):
        return self.title
    
    def get_tags_list(self):
        return [tag.strip() for tag in self.tags.split(',') if tag.strip()]
    
    def word_count(self):
        return len(self.content.split())

class FlashcardDeck(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    subject = models.CharField(max_length=50, choices=Note.SUBJECT_CHOICES, blank=True)
    is_public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return self.name
    
    def card_count(self):
        return self.cards.count()

class Flashcard(models.Model):
    deck = models.ForeignKey(FlashcardDeck, on_delete=models.CASCADE, related_name='cards')
    question = models.TextField()
    answer = models.TextField()
    hint = models.TextField(blank=True, help_text="Optional hint for the question")
    difficulty = models.CharField(max_length=20, choices=[
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ], default='medium')
    image = models.ImageField(upload_to='flashcards/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    order = models.PositiveIntegerField(default=0, help_text="Order within the deck")

    class Meta:
        ordering = ['order', 'created_at']

    def __str__(self):
        return f"{self.deck.name} - {self.question[:50]}"

class JournalEntry(models.Model):
    MOOD_CHOICES = [
        ('happy', '😊 Happy'),
        ('content', '😌 Content'),
        ('neutral', '😐 Neutral'),
        ('sad', '😢 Sad'),
        ('stressed', '😰 Stressed'),
        ('excited', '🤩 Excited'),
        ('tired', '😴 Tired'),
        ('anxious', '😟 Anxious'),
        ('grateful', '🙏 Grateful'),
        ('motivated', '💪 Motivated'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200, blank=True, help_text="Optional title for your entry")
    content = models.TextField()
    mood = models.CharField(max_length=20, choices=MOOD_CHOICES, default='neutral')
    tags = models.CharField(max_length=300, blank=True, help_text="Comma-separated tags")
    is_private = models.BooleanField(default=True, help_text="Keep this entry private")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Journal Entries"

    def __str__(self):
        if self.title:
            return f"{self.title} - {self.created_at.strftime('%Y-%m-%d')}"
        return f"Journal Entry - {self.created_at.strftime('%Y-%m-%d')}"
    
    def word_count(self):
        return len(self.content.split())

class StudySession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=50, choices=Note.SUBJECT_CHOICES)
    duration_minutes = models.PositiveIntegerField(help_text="Study session duration in minutes")
    notes_reviewed = models.ManyToManyField(Note, blank=True)
    flashcard_decks_used = models.ManyToManyField(FlashcardDeck, blank=True)
    session_type = models.CharField(max_length=20, choices=[
        ('reading', 'Reading'),
        ('flashcards', 'Flashcards'),
        ('practice', 'Practice Questions'),
        ('review', 'Review'),
        ('exam_prep', 'Exam Preparation'),
    ], default='reading')
    productivity_rating = models.IntegerField(choices=[
        (1, '1 - Poor'),
        (2, '2 - Below Average'),
        (3, '3 - Average'),
        (4, '4 - Good'),
        (5, '5 - Excellent'),
    ], null=True, blank=True)
    notes_text = models.TextField(blank=True, help_text="Session notes and reflections")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.get_subject_display()} - {self.duration_minutes}min - {self.created_at.strftime('%Y-%m-%d')}"

class TulipVariety(models.Model):
    name = models.CharField(max_length=100)
    scientific_name = models.CharField(max_length=100)
    description = models.TextField()
    color = models.CharField(max_length=50)
    bloom_time = models.CharField(max_length=50)
    height = models.CharField(max_length=50)
    care_instructions = models.TextField()
    image_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Tulip Varieties"
        ordering = ['name']

    def __str__(self):
        return self.name

class ClinicalSkill(models.Model):
    SKILL_CATEGORIES = [
        ('basic', 'Basic Nursing Skills'),
        ('assessment', 'Assessment Skills'),
        ('medication', 'Medication Administration'),
        ('procedures', 'Clinical Procedures'),
        ('emergency', 'Emergency Skills'),
        ('communication', 'Communication Skills'),
    ]
    
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=50, choices=SKILL_CATEGORIES)
    description = models.TextField()
    steps = models.TextField(help_text="Step-by-step procedure")
    safety_considerations = models.TextField()
    equipment_needed = models.TextField()
    competency_level = models.CharField(max_length=20, choices=[
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ], default='beginner')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['category', 'name']
    
    def __str__(self):
        return self.name

class StudyPlan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    semester = models.CharField(max_length=50)
    year = models.IntegerField()
    subjects = models.ManyToManyField('Note', through='StudyPlanSubject')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Study Plan - {self.semester} {self.year}"
class StudyPlanSubject(models.Model):
    study_plan = models.ForeignKey(StudyPlan, on_delete=models.CASCADE)
    subject = models.ForeignKey('Note', on_delete=models.CASCADE)
    priority = models.IntegerField(default=1)
    target_hours = models.IntegerField(default=10)
    completed_hours = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.subject} in {self.study_plan}"

    
class NCLEXQuestion(models.Model):
    QUESTION_TYPES = [
        ('multiple_choice', 'Multiple Choice'),
        ('select_all', 'Select All That Apply'),
        ('fill_blank', 'Fill in the Blank'),
        ('drag_drop', 'Drag and Drop'),
    ]
    
    question_text = models.TextField()
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPES, default='multiple_choice')
    options = models.JSONField(default=list)  # For multiple choice options
    correct_answers = models.JSONField(default=list)
    rationale = models.TextField()
    category = models.CharField(max_length=100)
    difficulty = models.CharField(max_length=20, choices=[
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ], default='medium')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['category', 'difficulty']
    
    def __str__(self):
        return f"NCLEX Question - {self.category}"