from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import (
    Note, FlashcardDeck, Flashcard, JournalEntry, 
    TulipVariety, ClinicalSkill, NCLEXQuestion, StudySession
)
from django.utils import timezone
import random

class Command(BaseCommand):
    help = 'Create sample data for the Bloom platform'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample data...')
        
        # Create sample users
        users = []
        for i in range(3):
            user, created = User.objects.get_or_create(
                username=f'student{i+1}',
                defaults={
                    'email': f'student{i+1}@example.com',
                    'first_name': f'Student',
                    'last_name': f'{i+1}'
                }
            )
            if created:
                user.set_password('password123')
                user.save()
            users.append(user)
        
        # Create sample notes
        sample_notes = [
            {
                'title': 'Cardiovascular System Overview',
                'subject': 'anatomy_physiology',
                'content': '''The cardiovascular system consists of the heart, blood vessels, and blood. 
                
Key Components:
- Heart: Four-chambered muscular pump
- Arteries: Carry oxygenated blood away from heart
- Veins: Return deoxygenated blood to heart
- Capillaries: Site of gas and nutrient exchange

Heart Chambers:
- Right Atrium: Receives deoxygenated blood
- Right Ventricle: Pumps blood to lungs
- Left Atrium: Receives oxygenated blood from lungs
- Left Ventricle: Pumps blood to body

Cardiac Cycle:
1. Diastole: Heart relaxes and fills
2. Systole: Heart contracts and pumps''',
                'tags': 'heart, circulation, anatomy, physiology',
                'priority': 'high'
            },
            {
                'title': 'Medication Administration Rights',
                'subject': 'pharmacology',
                'content': '''The 5 Rights of Medication Administration:

1. Right Patient
   - Check patient identification
   - Use two identifiers (name, DOB, MRN)
   - Verify with patient verbally

2. Right Medication
   - Check medication label three times
   - Verify against MAR
   - Check for allergies

3. Right Dose
   - Calculate dosage carefully
   - Use appropriate measuring devices
   - Double-check calculations

4. Right Route
   - Oral, IV, IM, subcutaneous, topical
   - Ensure route is appropriate for medication
   - Use proper technique

5. Right Time
   - Administer within 30 minutes of scheduled time
   - Consider medication interactions
   - Document administration time''',
                'tags': 'medication, safety, nursing, administration',
                'priority': 'urgent'
            },
            {
                'title': 'Infection Control Principles',
                'subject': 'fundamentals',
                'content': '''Standard Precautions:
- Hand hygiene before and after patient contact
- Use of personal protective equipment (PPE)
- Safe injection practices
- Respiratory hygiene/cough etiquette

Chain of Infection:
1. Infectious agent (pathogen)
2. Reservoir (where pathogen lives)
3. Portal of exit (how pathogen leaves reservoir)
4. Mode of transmission (how pathogen spreads)
5. Portal of entry (how pathogen enters new host)
6. Susceptible host (person who can get infected)

Breaking the Chain:
- Hand hygiene
- Sterilization and disinfection
- Isolation precautions
- Vaccination
- Proper waste disposal''',
                'tags': 'infection control, safety, precautions',
                'priority': 'high'
            }
        ]
        
        for note_data in sample_notes:
            user = random.choice(users)
            Note.objects.get_or_create(
                title=note_data['title'],
                user=user,
                defaults={
                    'subject': note_data['subject'],
                    'content': note_data['content'],
                    'tags': note_data['tags'],
                    'priority': note_data['priority'],
                    'is_public': True
                }
            )
        
        # Create sample flashcard decks
        deck_data = [
            {
                'name': 'Nursing Fundamentals',
                'description': 'Essential nursing concepts and procedures',
                'subject': 'fundamentals',
                'cards': [
                    {
                        'question': 'What are the 5 rights of medication administration?',
                        'answer': 'Right patient, Right medication, Right dose, Right route, Right time',
                        'difficulty': 'medium'
                    },
                    {
                        'question': 'Define therapeutic communication',
                        'answer': 'A purposeful form of communication that allows patients to express feelings and promotes healing relationships.',
                        'difficulty': 'easy'
                    },
                    {
                        'question': 'What is the nursing process?',
                        'answer': 'A systematic approach to patient care: Assessment, Diagnosis, Planning, Implementation, Evaluation (ADPIE)',
                        'difficulty': 'easy'
                    }
                ]
            },
            {
                'name': 'Pharmacology Basics',
                'description': 'Key drug classifications and nursing considerations',
                'subject': 'pharmacology',
                'cards': [
                    {
                        'question': 'ACE Inhibitors - Common suffix and action',
                        'answer': 'Suffix: -pril (lisinopril). Action: Block conversion of angiotensin I to II, reducing blood pressure.',
                        'difficulty': 'medium'
                    },
                    {
                        'question': 'Beta Blockers - Common suffix and nursing considerations',
                        'answer': 'Suffix: -lol (metoprolol). Monitor heart rate and blood pressure. Do not stop abruptly.',
                        'difficulty': 'medium'
                    }
                ]
            }
        ]
        
        for deck_info in deck_data:
            user = random.choice(users)
            deck, created = FlashcardDeck.objects.get_or_create(
                name=deck_info['name'],
                user=user,
                defaults={
                    'description': deck_info['description'],
                    'subject': deck_info['subject'],
                    'is_public': True
                }
            )
            
            if created:
                for i, card_data in enumerate(deck_info['cards']):
                    Flashcard.objects.create(
                        deck=deck,
                        question=card_data['question'],
                        answer=card_data['answer'],
                        difficulty=card_data['difficulty'],
                        order=i
                    )
        
        # Create sample journal entries
        journal_entries = [
            {
                'title': 'First Clinical Day',
                'content': 'Today was my first day in clinical rotation. I was nervous but excited. The nurses were very welcoming and helped me feel comfortable. I observed several procedures and took detailed notes.',
                'mood': 'excited',
                'tags': 'clinical, first day, nervous, learning'
            },
            {
                'title': 'Challenging Study Session',
                'content': 'Spent 3 hours studying pharmacology today. The drug classifications are starting to make more sense, but I still need more practice with dosage calculations.',
                'mood': 'content',
                'tags': 'study, pharmacology, dosage calculations'
            }
        ]
        
        for entry_data in journal_entries:
            user = random.choice(users)
            JournalEntry.objects.get_or_create(
                title=entry_data['title'],
                user=user,
                defaults={
                    'content': entry_data['content'],
                    'mood': entry_data['mood'],
                    'tags': entry_data['tags'],
                    'is_private': False
                }
            )
        
        # Create sample study sessions
        for user in users:
            for i in range(5):
                StudySession.objects.get_or_create(
                    user=user,
                    subject=random.choice(['fundamentals', 'pharmacology', 'anatomy_physiology']),
                    defaults={
                        'duration_minutes': random.randint(30, 180),
                        'session_type': random.choice(['reading', 'flashcards', 'practice', 'review']),
                        'productivity_rating': random.randint(3, 5),
                        'notes_text': f'Study session {i+1} notes and reflections.'
                    }
                )
        
        self.stdout.write(
            self.style.SUCCESS('Successfully created sample data!')
        )