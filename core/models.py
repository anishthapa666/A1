from django.db import models
from django.contrib.auth.models import User

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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class FlashcardDeck(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Flashcard(models.Model):
    deck = models.ForeignKey(FlashcardDeck, on_delete=models.CASCADE, related_name='cards')
    question = models.TextField()
    answer = models.TextField()
    image = models.ImageField(upload_to='flashcards/', blank=True, null=True)

    def __str__(self):
        return f"{self.deck.name} - {self.question[:50]}"

class JournalEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    content = models.TextField()
    mood = models.CharField(max_length=20, choices=[
        ('happy', 'Happy'),
        ('content', 'Content'),
        ('neutral', 'Neutral'),
        ('sad', 'Sad'),
        ('stressed', 'Stressed'),
    ], default='neutral')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Journal Entry - {self.created_at.strftime('%Y-%m-%d')}"

class TulipVariety(models.Model):
    name = models.CharField(max_length=100)
    scientific_name = models.CharField(max_length=100)
    description = models.TextField()
    color = models.CharField(max_length=50)
    bloom_time = models.CharField(max_length=50)
    height = models.CharField(max_length=50)
    care_instructions = models.TextField()
    image_url = models.URLField(blank=True)

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
    
    def __str__(self):
        return f"NCLEX Question - {self.category}"