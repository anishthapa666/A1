from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse, Http404, FileResponse
from django.conf import settings
from .models import Note, FlashcardDeck, Flashcard, JournalEntry, TulipVariety, ClinicalSkill, NCLEXQuestion
import json
import random
import os
import io
from django.contrib.staticfiles import finders
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def home(request):
    return render(request, 'core/home.html')

def photobooth(request):
    return render(request, 'core/photobooth.html')

def tulips(request):
    tulip_varieties = TulipVariety.objects.all()
    if not tulip_varieties.exists():
        # Create some sample tulip data
        sample_tulips = [
    {
        'name': 'Red Emperor',
        'scientific_name': 'Tulipa fosteriana',
        'description': 'Large, brilliant red blooms that open wide in the sun. One of the earliest tulips to bloom.',
        'color': 'Bright Red',
        'bloom_time': 'Early Spring',
        'height': '12-16 inches',
        'care_instructions': 'Plant in well-drained soil in full sun to partial shade. Water regularly during growing season.',
        'image_url': 'https://i.pinimg.com/1200x/5b/ec/1d/5bec1db2f047e4ae6b560d658753fe8b.jpg?auto=compress&cs=tinysrgb&h=300'
    },
    {
        'name': 'Queen of Night',
        'scientific_name': 'Tulipa',
        'description': 'Deep purple-black blooms that are almost black in certain light. A dramatic and elegant variety.',
        'color': 'Deep Purple-Black',
        'bloom_time': 'Late Spring',
        'height': '18-24 inches',
        'care_instructions': 'Prefers full sun and well-drained, fertile soil. Allow foliage to die back naturally.',
        'image_url': 'https://i.pinimg.com/736x/5f/f6/24/5ff6240c04a1177852c18e6d46d74f51.jpg?auto=compress&cs=tinysrgb&h=300'
    },
    {
        'name': 'White Dream',
        'scientific_name': 'Tulipa triumph',
        'description': 'Pure white petals with a subtle cream center. Perfect for creating elegant spring displays.',
        'color': 'Pure White',
        'bloom_time': 'Mid Spring',
        'height': '14-18 inches',
        'care_instructions': 'Plant bulbs 6-8 inches deep in fall. Mulch in winter for protection in cold climates.',
        'image_url': 'https://i.pinimg.com/736x/a8/4a/d1/a84ad1748a0065718ef3ce3cd63a1819.jpg?auto=compress&cs=tinysrgb&h=300'
    },
    {
        'name': 'Pink Impression',
        'scientific_name': 'Tulipa darwin hybrid',
        'description': 'Large, soft pink blooms on strong stems. Excellent for cut flowers and naturalizing.',
        'color': 'Soft Pink',
        'bloom_time': 'Mid to Late Spring',
        'height': '20-24 inches',
        'care_instructions': 'Very hardy variety. Plant in full sun with good drainage. Fertilize in early spring.',
        'image_url': 'https://i.pinimg.com/736x/d1/5f/12/d15f1284150bc1efa38037610042c247.jpg?auto=compress&cs=tinysrgb&h=300'
    },
    {
        'name': 'Yellow Crown',
        'scientific_name': 'Tulipa single early',
        'description': 'Bright yellow petals with a sunny disposition. One of the most cheerful spring bloomers.',
        'color': 'Bright Yellow',
        'bloom_time': 'Early to Mid Spring',
        'height': '12-15 inches',
        'care_instructions': 'Excellent for containers and rock gardens. Water well during growth period.',
        'image_url': 'https://i.pinimg.com/1200x/84/8c/64/848c64e17faea3f6df901f8aaa329810.jpg?auto=compress&cs=tinysrgb&h=300'
    },
    {
        'name': 'Purple Prince',
        'scientific_name': 'Tulipa single late',
        'description': 'Rich purple blooms with a velvety texture. Creates stunning mass plantings.',
        'color': 'Rich Purple',
        'bloom_time': 'Late Spring',
        'height': '18-22 inches',
        'care_instructions': 'Plant in groups for best effect. Deadhead after blooming but leave foliage intact.',
        'image_url': 'https://i.pinimg.com/1200x/ad/e9/ab/ade9ab65b34a8a590e9b6fab8c7fcd9c.jpg?auto=compress&cs=tinysrgb&h=300'
    }
    ]

        
        
        for tulip_data in sample_tulips:
            TulipVariety.objects.create(**tulip_data)
        
        tulip_varieties = TulipVariety.objects.all()
    
    context = {'tulip_varieties': tulip_varieties}
    return render(request, 'core/tulips.html', context)

def games(request):
    return render(request, 'core/games.html')

def memory_game(request):
    return render(request, 'core/memory_game.html')

def quiz_game(request):
    # Mix of general nursing and tulip questions for variety
    nursing_questions = [
        {
            'question': 'What is the normal range for adult heart rate?',
            'options': ['40-60 bpm', '60-100 bpm', '100-120 bpm', '120-140 bpm'],
            'correct': 1
        },
        {
            'question': 'Which vital sign should be assessed first in an emergency?',
            'options': ['Temperature', 'Blood Pressure', 'Airway/Breathing', 'Pulse'],
            'correct': 2
        },
        {
            'question': 'What does the acronym ADPIE stand for in nursing process?',
            'options': ['Assess, Diagnose, Plan, Implement, Evaluate', 'Analyze, Develop, Perform, Inspect, Execute', 'Admit, Discharge, Plan, Intervene, Educate', 'Assess, Document, Prescribe, Inject, Examine'],
            'correct': 0
        },
        {
            'question': 'Which position is best for a patient with difficulty breathing?',
            'options': ['Supine', 'Prone', 'Fowler\'s', 'Trendelenburg'],
            'correct': 2
        },
        {
            'question': 'What is the most common route for medication administration?',
            'options': ['Intravenous', 'Intramuscular', 'Oral', 'Subcutaneous'],
            'correct': 2
        },
        {
            'question': 'What country is famous for tulip cultivation?',
            'options': ['France', 'Netherlands', 'Germany', 'Italy'],
            'correct': 1
        },
    ]
    
    # Randomly select 5 questions
    selected_questions = random.sample(nursing_questions, min(5, len(nursing_questions)))
    context = {'questions': json.dumps(selected_questions)}
    return render(request, 'core/quiz_game.html', context)

def puzzle_game(request):
    return render(request, 'core/puzzle_game.html')

def word_search(request):
    return render(request, 'core/word_search.html')

def garden_designer(request):
    return render(request, 'core/garden_designer.html')

def study_companion(request):
    if request.method == 'POST':
        content = request.POST.get('journal_content', '')
        mood = request.POST.get('mood', 'neutral')
        if content:
            JournalEntry.objects.create(content=content, mood=mood)
        return JsonResponse({'success': True})
    
    recent_entries = JournalEntry.objects.order_by('-created_at')[:5]
    return render(request, 'core/study_companion.html', {'recent_entries': recent_entries})

def notes(request):
    notes = Note.objects.all().order_by('-created_at')
    subjects = Note.SUBJECT_CHOICES
    return render(request, 'core/notes.html', {'notes': notes, 'subjects': subjects})

def notes_history(request):
    notes = Note.objects.all().order_by('-created_at')
    return render(request, 'core/notes_history.html', {'notes': notes})

def create_note(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        subject = request.POST.get('subject')
        
        if title and content and subject:
            note = Note.objects.create(
                title=title,
                content=content,
                subject=subject,
                user=request.user if request.user.is_authenticated else None
            )
            return JsonResponse({'success': True, 'note_id': note.id})
        return JsonResponse({'success': False, 'error': 'Missing required fields'})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

def view_note(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    return render(request, 'core/view_note.html', {'note': note})

def flashcards(request):
    decks = FlashcardDeck.objects.all()
    if not decks.exists():
        # Create nursing-focused sample decks
        fundamentals_deck = FlashcardDeck.objects.create(
            name='Nursing Fundamentals',
            description='Essential concepts every nursing student should master.'
        )
        
        fundamentals_cards = [
            {
                'question': 'What are the 5 rights of medication administration?',
                'answer': 'Right patient, Right medication, Right dose, Right route, Right time'
            },
            {
                'question': 'Define therapeutic communication',
                'answer': 'A purposeful form of communication that allows patients to express feelings and promotes healing relationships.'
            },
            {
                'question': 'What is the nursing process?',
                'answer': 'A systematic approach to patient care: Assessment, Diagnosis, Planning, Implementation, Evaluation (ADPIE)'
            },
            {
                'question': 'Normal adult blood pressure range',
                'answer': 'Systolic: 90-120 mmHg, Diastolic: 60-80 mmHg'
            }
        ]
        
        for card_data in fundamentals_cards:
            Flashcard.objects.create(deck=fundamentals_deck, **card_data)
            
        # Create pharmacology deck
        pharm_deck = FlashcardDeck.objects.create(
            name='Pharmacology Essentials',
            description='Key drug classifications and nursing considerations.'
        )
        
        pharm_cards = [
            {
                'question': 'ACE Inhibitors - Common suffix and action',
                'answer': 'Suffix: -pril (lisinopril). Action: Block conversion of angiotensin I to II, reducing blood pressure.'
            },
            {
                'question': 'Beta Blockers - Common suffix and nursing considerations',
                'answer': 'Suffix: -lol (metoprolol). Monitor heart rate and blood pressure. Do not stop abruptly.'
            },
            {
                'question': 'Diuretics - Main types and nursing considerations',
                'answer': 'Loop, thiazide, potassium-sparing. Monitor electrolytes, especially potassium. Assess for dehydration.'
            }
        ]
        
        for card_data in pharm_cards:
            Flashcard.objects.create(deck=pharm_deck, **card_data)
        
        decks = FlashcardDeck.objects.all()
    
    return render(request, 'core/flashcards.html', {'decks': decks})

def clinical_skills(request):
    skills = ClinicalSkill.objects.all()
    if not skills.exists():
        # Create sample clinical skills
        sample_skills = [
            {
                'name': 'Hand Hygiene',
                'category': 'basic',
                'description': 'Proper handwashing technique to prevent infection transmission',
                'steps': '1. Wet hands with water\n2. Apply soap\n3. Rub hands together for 20 seconds\n4. Rinse thoroughly\n5. Dry with clean towel',
                'safety_considerations': 'Use alcohol-based sanitizer when soap unavailable. Remove jewelry before washing.',
                'equipment_needed': 'Soap, running water, clean towel or paper towels',
                'competency_level': 'beginner'
            },
            {
                'name': 'Blood Pressure Measurement',
                'category': 'assessment',
                'description': 'Accurate measurement of systolic and diastolic blood pressure',
                'steps': '1. Position patient comfortably\n2. Select appropriate cuff size\n3. Place cuff 1 inch above antecubital fossa\n4. Inflate cuff 20-30 mmHg above palpated systolic\n5. Deflate slowly at 2-3 mmHg per second\n6. Record first and last Korotkoff sounds',
                'safety_considerations': 'Ensure proper cuff size. Wait 1-2 minutes between measurements.',
                'equipment_needed': 'Sphygmomanometer, stethoscope, appropriate sized cuff',
                'competency_level': 'beginner'
            },
            {
                'name': 'IV Insertion',
                'category': 'procedures',
                'description': 'Sterile insertion of intravenous catheter',
                'steps': '1. Verify order and patient identity\n2. Gather supplies\n3. Perform hand hygiene\n4. Apply tourniquet\n5. Cleanse site with antiseptic\n6. Insert catheter at 15-30 degree angle\n7. Advance catheter and remove needle\n8. Secure and document',
                'safety_considerations': 'Maintain sterile technique. Check for allergies. Monitor for infiltration.',
                'equipment_needed': 'IV catheter, antiseptic, tourniquet, tape, IV tubing, saline flush',
                'competency_level': 'intermediate'
            }
        ]
        
        for skill_data in sample_skills:
            ClinicalSkill.objects.create(**skill_data)
        
        skills = ClinicalSkill.objects.all()
    
    return render(request, 'core/clinical_skills.html', {'skills': skills})

def nclex_prep(request):
    questions = NCLEXQuestion.objects.all()
    if not questions.exists():
        # Create sample NCLEX questions
        sample_questions = [
            {
                'question_text': 'A client with heart failure is prescribed furosemide (Lasix). Which assessment finding indicates the medication is effective?',
                'question_type': 'multiple_choice',
                'options': ['Decreased urine output', 'Increased weight', 'Decreased edema', 'Increased blood pressure'],
                'correct_answers': [2],
                'rationale': 'Furosemide is a loop diuretic that removes excess fluid, reducing edema in heart failure patients.',
                'category': 'Pharmacology',
                'difficulty': 'medium'
            },
            {
                'question_text': 'Which actions should the nurse take when caring for a client with a seizure disorder? Select all that apply.',
                'question_type': 'select_all',
                'options': ['Place client in supine position', 'Insert oral airway during seizure', 'Time the duration of seizure', 'Protect client from injury', 'Administer oxygen as needed'],
                'correct_answers': [2, 3, 4],
                'rationale': 'During seizures, protect from injury, time duration, and provide oxygen if needed. Never force objects in mouth or place flat on back.',
                'category': 'Medical-Surgical',
                'difficulty': 'hard'
            }
        ]
        
        for question_data in sample_questions:
            NCLEXQuestion.objects.create(**question_data)
        
        questions = NCLEXQuestion.objects.all()
    
    # Select random questions for practice
    practice_questions = random.sample(list(questions), min(10, len(questions)))
    return render(request, 'core/nclex_prep.html', {'questions': practice_questions})

def nursing_curriculum(request):
    return render(request, 'core/nursing_curriculum.html')

def download_notes(request, subject):
    """Generate and download PDF notes for a specific subject"""
    
    # Subject content mapping
    subject_content = {
        'anatomy': {
            'title': 'Human Anatomy - Complete Notes',
            'chapters': [
                'Introduction to Anatomy',
                'Skeletal System',
                'Muscular System', 
                'Cardiovascular System',
                'Respiratory System',
                'Nervous System',
                'Digestive System',
                'Urinary System'
            ]
        },
        'physiology': {
            'title': 'Human Physiology - Complete Notes',
            'chapters': [
                'Cell Physiology',
                'Cardiovascular Physiology',
                'Respiratory Physiology',
                'Renal Physiology',
                'Neurophysiology',
                'Endocrine System',
                'Digestive Physiology',
                'Reproductive Physiology'
            ]
        },
        'biochemistry': {
            'title': 'Biochemistry - Complete Notes',
            'chapters': [
                'Biomolecules',
                'Enzymes',
                'Carbohydrate Metabolism',
                'Lipid Metabolism',
                'Protein Metabolism',
                'Nucleic Acid Metabolism',
                'Clinical Biochemistry'
            ]
        },
        'fundamentals': {
            'title': 'Fundamentals of Nursing - Complete Notes',
            'chapters': [
                'Introduction to Nursing',
                'Nursing Process',
                'Communication',
                'Infection Control',
                'Vital Signs',
                'Medication Administration',
                'Documentation',
                'Patient Safety'
            ]
        }
    }
    
    if subject not in subject_content:
        raise Http404("Subject not found")
    
    content = subject_content[subject]
    
    # Create PDF
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    
    # Title page
    p.setFont("Helvetica-Bold", 24)
    p.drawString(100, height - 100, content['title'])
    p.setFont("Helvetica", 16)
    p.drawString(100, height - 140, "TU Institute of Medicine")
    p.drawString(100, height - 160, "B.Sc. Nursing Program")
    
    y_position = height - 220
    
    # Table of contents
    p.setFont("Helvetica-Bold", 18)
    p.drawString(100, y_position, "Table of Contents")
    y_position -= 40
    
    p.setFont("Helvetica", 12)
    for i, chapter in enumerate(content['chapters'], 1):
        p.drawString(120, y_position, f"{i}. {chapter}")
        y_position -= 20
        
        if y_position < 100:
            p.showPage()
            y_position = height - 100
    
    # Add sample content for first chapter
    p.showPage()
    y_position = height - 100
    
    p.setFont("Helvetica-Bold", 18)
    p.drawString(100, y_position, f"Chapter 1: {content['chapters'][0]}")
    y_position -= 40
    
    p.setFont("Helvetica", 12)
    sample_text = [
        "This chapter covers the fundamental concepts and principles.",
        "Key learning objectives:",
        "• Understand basic terminology",
        "• Identify key structures and functions", 
        "• Apply knowledge to clinical scenarios",
        "",
        "For complete notes, please refer to your textbooks and",
        "attend lectures regularly."
    ]
    
    for line in sample_text:
        p.drawString(100, y_position, line)
        y_position -= 20
    
    p.save()
    buffer.seek(0)
    
    response = FileResponse(
        buffer,
        as_attachment=True,
        filename=f'{subject}_notes.pdf',
        content_type='application/pdf'
    )
    
    return response

def download_questions(request, subject):
    """Generate and download past questions PDF for a specific subject"""
    
    # Sample questions for different subjects
    questions_data = {
        'anatomy': {
            'title': 'Human Anatomy - Past Questions',
            'questions': [
                {
                    'year': '2079',
                    'questions': [
                        'Define anatomical position. List the directional terms used in anatomy. (5 marks)',
                        'Describe the structure and functions of synovial joints. (10 marks)',
                        'Explain the blood supply of the heart. (8 marks)',
                        'Write short notes on: a) Nephron b) Alveoli (2×3=6 marks)'
                    ]
                },
                {
                    'year': '2078',
                    'questions': [
                        'Classify bones based on shape with examples. (6 marks)',
                        'Describe the anatomy of respiratory system. (12 marks)',
                        'Explain the structure of neuron. (7 marks)'
                    ]
                }
            ]
        },
        'physiology': {
            'title': 'Human Physiology - Past Questions',
            'questions': [
                {
                    'year': '2079',
                    'questions': [
                        'Explain the mechanism of muscle contraction. (10 marks)',
                        'Describe the cardiac cycle with diagram. (12 marks)',
                        'Write about regulation of blood pressure. (8 marks)'
                    ]
                }
            ]
        }
    }
    
    if subject not in questions_data:
        raise Http404("Questions not found")
    
    content = questions_data[subject]
    
    # Create PDF
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    
    # Title page
    p.setFont("Helvetica-Bold", 24)
    p.drawString(100, height - 100, content['title'])
    p.setFont("Helvetica", 16)
    p.drawString(100, height - 140, "TU Institute of Medicine")
    p.drawString(100, height - 160, "Board Examination Questions")
    
    y_position = height - 220
    
    # Questions by year
    for year_data in content['questions']:
        p.setFont("Helvetica-Bold", 16)
        p.drawString(100, y_position, f"Year {year_data['year']}")
        y_position -= 30
        
        p.setFont("Helvetica", 12)
        for i, question in enumerate(year_data['questions'], 1):
            # Wrap long questions
            words = question.split()
            line = f"{i}. "
            for word in words:
                if len(line + word) > 80:
                    p.drawString(100, y_position, line)
                    y_position -= 15
                    line = "   " + word + " "
                else:
                    line += word + " "
            
            if line.strip():
                p.drawString(100, y_position, line)
                y_position -= 25
            
            if y_position < 100:
                p.showPage()
                y_position = height - 100
        
        y_position -= 20
    
    p.save()
    buffer.seek(0)
    
    response = FileResponse(
        buffer,
        as_attachment=True,
        filename=f'{subject}_questions.pdf',
        content_type='application/pdf'
    )
    
    return response