from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
import re
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
from nltk.tokenize import word_tokenize
from docx import Document
import fitz  # PyMuPDF for PDF reading
import json 

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
import json
import re
import logging
import asyncio
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


from datetime import datetime, timedelta
import os





nltk.download('punkt')
# Configuration des e-mails et du bot Telegram
EMAIL_ADDRESS = 'cvupdz@gmail.com'
EMAIL_PASSWORD = 'avpu agry kuwj zlzs'
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
TELEGRAM_BOT_TOKEN = '7495077361:AAHDCDdyfUbOzoajombUut_r2k699jEiFWc'

# Chemins des fichiers CV
CV_FILES = {
    'junior': 'cv_models/Junior_cv_model.docx',
    'senior': 'cv_models/Senior_cv_model.docx'
}

# Chemin du fichier JSON pour les questions
QUESTIONS_FILE = 'questions.json'
# Chemin du fichier JSON pour les e-mails envoyés
SENT_EMAILS_FILE = 'my_telegram_bot/sent_emails.json'

# Liste des utilisateurs autorisés (administrateurs)
admin_user_ids = [1719899525, 987654321]  # Replace with actual user IDs

# async def webhook(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     # This function will handle incoming updates via webhook
#     await application.process_update(update)

def read_docx(file_path):
    """
    Reads a .docx file and returns the extracted text.
    
    Parameters:
    file_path (str): The path to the .docx file.
    
    Returns:
    str: The full text extracted from the document.
    """
    try:
        doc = Document(file_path)
        full_text = []
        for para in doc.paragraphs:
            full_text.append(para.text)
        return '\n'.join(full_text)
    except Exception as e:
        raise ValueError(f"Error reading .docx file: {e}")

def read_pdf(file_path):
    """
    Reads a .pdf file and returns the extracted text.
    
    Parameters:
    file_path (str): The path to the .pdf file.
    
    Returns:
    str: The full text extracted from the PDF.
    """
    try:
        doc = fitz.open(file_path)
        full_text = []
        for page in doc:
            full_text.append(page.get_text())
        return '\n'.join(full_text)
    except Exception as e:
        raise ValueError(f"Error reading PDF file: {e}")
    
def analyze_resume(file_path):
    """
    Analyzes a resume by extracting and evaluating various sections and elements.
    
    Parameters:
    file_path (str): The path to the resume file (.docx or .pdf).
    
    Returns:
    str: A formatted string containing the analysis results for different resume sections.
    """
    # Determine the file format and extract the text
    if file_path.endswith('.docx'):
        text = read_docx(file_path)
    elif file_path.endswith('.pdf'):
        text = read_pdf(file_path)
    else:
        raise ValueError("Unsupported file format. Please upload a .docx or .pdf file.")
    
    # Initialize the feedback dictionary
    feedback = {}
    tfidf = TfidfVectorizer()

    # Convert text to lowercase and tokenize
    lowercase_text = text.lower()
    tokens = tokenize(lowercase_text)

    # Perform various analyses on the resume content
    feedback['contact_info'] = check_contact_info(text)
    feedback['summary'] = analyze_summary(lowercase_text)
    feedback['education'] = analyze_education(lowercase_text)
    feedback['work_experience'] = analyze_work_experience(lowercase_text)
    feedback['skills'] = analyze_skills(lowercase_text, tokens, tfidf)
    feedback['structure'] = analyze_structure(text)
    feedback['achievements'] = analyze_achievements(lowercase_text)
    feedback['language'] = analyze_language(tokens)
    feedback['keywords'] = analyze_keywords(lowercase_text, tfidf)
    feedback['certifications'] = analyze_certifications(lowercase_text)
    feedback['projects'] = analyze_projects(lowercase_text)
    feedback['volunteer_experience'] = analyze_volunteer_experience(lowercase_text)
    feedback['interests'] = analyze_interests(lowercase_text)
    feedback['references'] = analyze_references(lowercase_text)
    feedback['formatting'] = analyze_formatting(text)
    feedback['professional_development'] = analyze_professional_development(lowercase_text)
    feedback['publications'] = analyze_publications(lowercase_text)
    feedback['technical_skills'] = analyze_technical_skills(lowercase_text)
    feedback['languages'] = analyze_language_proficiencies(lowercase_text)
    feedback['online_presence'] = analyze_online_presence(text)
    feedback['awards'] = analyze_awards_and_honors(lowercase_text)
    feedback['industry_specific'] = analyze_industry_specific_elements(lowercase_text)
    feedback['overall_assessment'] = provide_overall_assessment(feedback)
    
    return feedback




# print(generate_report(formatted_reports))

def tokenize(text):
    """
    Tokenizes the text into words using NLTK.
    
    Parameters:
    text (str): The text to tokenize.
    
    Returns:
    list: A list of tokens (words).
    """
    return word_tokenize(text)

def check_contact_info(text):
    """
    Checks for the presence of contact information (email and phone number) in the text.
    
    Parameters:
    text (str): The text to analyze.
    
    Returns:
    dict: A dictionary with detected email and phone number.
    """
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    phone_pattern = r'\b(\+\d{1,2}\s?)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}\b|\+\d{3}\s\d{3}\s\d{3}\s\d{3}\b'

    
    
    email = re.search(email_pattern, text)
    phone = re.search(phone_pattern, text)
    
    return {
        'exists': email_pattern and phone_pattern
    }

def analyze_summary(text):
    """
    Analyzes the summary or objective section of the resume.
    
    Parameters:
    text (str): The text to analyze.
    
    Returns:
    dict: A dictionary indicating the presence and length of the summary.
    """
    summary_keywords = ['summary', 'objective', 'profile']
    has_summary = any(keyword in text for keyword in summary_keywords)
    return {
        'exists': has_summary,
        'length': len(text.split()) if has_summary else 0
    }

def analyze_education(text):
    """
    Analyzes the education section of the resume.

    Parameters:
    text (str): The text to analyze.

    Returns:
    dict: A dictionary indicating the presence and details of the education section.
    """
    # Define keywords and patterns
    education_keywords = ['éducation', 'diplôme', 'université', 'collège', 'bachelor', 'master', 'doctorat', 'diplôme', 'certificat', 'école', 'institut', 'académie']
    degree_types = ['associate', 'bachelor', 'master', 'doctorat', 'phd', 'mba', 'bsc', 'ba', 'ms', 'ma']
    institution_keywords = ['université', 'collège', 'institut', 'école', 'académie']
    year_pattern = re.compile(r'\b(19|20)\d{2}\b')
    gpa_pattern = re.compile(r'gpa\s*[:=]?\s*([0-4]\.?\d*)', re.IGNORECASE)
    coursework_keywords = ['cours', 'cours pertinents', 'principaux cours', 'majeure', 'mineure', 'concentration']
    achievement_keywords = ['honor', 'prix', 'bourse', 'liste du doyen', 'cum laude', 'magna cum laude', 'summa cum laude', 'distinction', 'mérite']
    international_keywords = ['études à l\'étranger', 'international', 'programme d\'échange']
    ongoing_education_keywords = ['en cours', 'actuel', 'en progression', 'graduation attendue']

    # Normalize text to lower case
    text_lower = text.lower()

    # Check for education keywords
    has_education = any(keyword in text_lower for keyword in education_keywords)
    feedback = []
    score = 0
    suggestions = []

    if not has_education:
        return {
            'exists': has_education,
            'details': 'Aucune section éducation claire trouvée',
            'text': "Oups ! Il semble que votre parcours académique soit absent du CV. Mettez en avant votre parcours éducatif - diplômes, institutions, dates de graduation et toute réalisation académique remarquable. Montrez-nous vos compétences !",
            'score': 0,
            'suggestions': ["Ajoutez une section 'Éducation' à votre CV", "Incluez tous les diplômes et certifications pertinents"]
        }

    # Check for degree types
    found_degrees = [degree for degree in degree_types if degree in text_lower]
    if not found_degrees:
        feedback.append("N'hésitez pas à mentionner votre diplôme ! Indiquez clairement le type de diplôme que vous avez obtenu.")
        suggestions.append("Précisez le(s) type(s) de diplôme")
    else:
        score += 0.2
        if len(found_degrees) > 1:
            score += 0.1  # Bonus pour plusieurs diplômes

    # Check for institutions
    has_institution = any(keyword in text_lower for keyword in institution_keywords)
    if not has_institution:
        feedback.append("Où avez-vous étudié ? Assurez-vous d'inclure le nom de vos institutions éducatives.")
        suggestions.append("Ajoutez le(s) nom(s) de vos institutions éducatives")
    else:
        score += 0.15

    # Check for graduation years
    graduation_years = year_pattern.findall(text)
    if not graduation_years:
        feedback.append("Ajoutez des dates ! Indiquer vos années de graduation aide à comprendre votre parcours académique.")
        suggestions.append("Incluez l'année de graduation pour chaque diplôme")
    else:
        score += 0.15
        if len(graduation_years) > 1:
            score += 0.05  # Bonus pour plusieurs années de graduation

    # Check for GPA
    gpa_match = gpa_pattern.search(text)
    if not gpa_match:
        feedback.append("Si vous avez un GPA de 3.5 ou plus, ne le gardez pas secret ! C'est un excellent moyen de montrer vos compétences académiques.")
        suggestions.append("Envisagez d'ajouter votre GPA s'il est de 3.5 ou plus")
    else:
        gpa = float(gpa_match.group(1))
        if gpa >= 3.5:
            score += 0.2
        elif gpa >= 3.0:
            score += 0.1

    # Check for relevant coursework
    has_coursework = any(keyword in text_lower for keyword in coursework_keywords)
    if not has_coursework:
        feedback.append("Pour vraiment impressionner, ajoutez des cours pertinents qui correspondent aux exigences du poste. C'est comme assaisonner académiquement !")
        suggestions.append("Ajoutez des cours pertinents ou des domaines de concentration")
    else:
        score += 0.15

    # Check for academic achievements
    found_achievements = [achievement for achievement in achievement_keywords if achievement in text_lower]
    if not found_achievements:
        feedback.append("Avez-vous obtenu des distinctions académiques ? Ne soyez pas modeste - listez ces honneurs, prix ou bourses !")
        suggestions.append("Incluez des réalisations académiques, des honneurs ou des prix")
    else:
        score += 0.15
        if len(found_achievements) > 1:
            score += 0.1  # Bonus pour plusieurs réalisations

    # Check for study abroad or international education
    has_international_experience = any(keyword in text_lower for keyword in international_keywords)
    if has_international_experience:
        score += 0.1
        feedback.append("Excellent travail en mettant en avant votre expérience internationale ! Cela peut vraiment vous démarquer.")

    # Check for ongoing education or professional development
    has_ongoing_education = any(keyword in text_lower for keyword in ongoing_education_keywords)
    if has_ongoing_education:
        score += 0.1
        feedback.append("Excellent travail en mentionnant votre éducation continue. Cela montre votre engagement envers l'apprentissage continu !")

    # Normalize score to be between 0 and 1
    score = min(score, 1)

    # Generate overall feedback
    if score < 0.3:
        overall_feedback = "Votre section éducation a besoin d'une attention sérieuse. Renforcez-la pour vraiment mettre en valeur votre parcours académique !"
    elif score < 0.6:
        overall_feedback = "Vous êtes sur la bonne voie avec votre section éducation, mais il y a encore de la place pour l'amélioration. Ajoutez plus de détails pour la faire briller !"
    elif score < 0.9:
        overall_feedback = "Bravo pour votre section éducation ! Quelques ajustements et elle sera parfaite."
    else:
        overall_feedback = "Wow ! Votre section éducation est excellente. Elle met vraiment en avant vos réalisations académiques et votre parcours pertinent."

    feedback_text = (f"{overall_feedback} Voici comment nous pouvons l'améliorer : {' '.join(feedback)} "
                     f"Souvenez-vous, votre section éducation est votre vitrine académique - faites-la ressortir !" if feedback else
                     f"{overall_feedback} Assurez-vous juste qu'elle est adaptée pour mettre en avant les aspects les plus pertinents pour le poste que vous visez.")

    return {
        'exists': has_education,
        'details': 'Section éducation trouvée' if has_education else 'Aucune section éducation claire trouvée',
        'text': feedback_text,
        'score': score,
        'suggestions': suggestions
    }

def analyze_work_experience(text):
    """
    Analyzes the work experience section of the resume.
    
    Parameters:
    text (str): The text to analyze.
    
    Returns:
    dict: A dictionary indicating the presence and details of the work experience section.
    """
    experience_keywords = ['experience', 'work history', 'employment']
    has_experience = any(keyword in text for keyword in experience_keywords)
    return {
        'exists': has_experience,
        'details': 'Work experience section found' if has_experience else 'No clear work experience section'
    }

def analyze_skills(text, tokens, tfidf):
    """
    Analyzes the skills section of the resume.
    
    Parameters:
    text (str): The text to analyze.
    tokens (list): A list of tokens (words) from the resume.
    tfidf (TfidfVectorizer): A TF-IDF vectorizer object for keyword analysis.
    
    Returns:
    dict: A dictionary indicating the presence and details of the skills section.
    """
    skill_keywords = ['skills', 'abilities', 'competencies']
    has_skills = any(keyword in text for keyword in skill_keywords)
    return {
        'exists': has_skills,
        'details': 'Skills section found' if has_skills else 'No clear skills section'
    }

def analyze_structure(text):
    """
    Analyzes the overall structure of the resume.
    
    Parameters:
    text (str): The text to analyze.
    
    Returns:
    dict: A dictionary indicating the presence of key sections and overall structure quality.
    """
    sections = ['summary', 'education', 'experience', 'skills']
    found_sections = [section for section in sections if section in text.lower()]
    return {
        'sections_found': found_sections,
        'well_structured': len(found_sections) >= 3
    }

def analyze_achievements(text):
    """
    Analyzes the achievements mentioned in the resume.
    
    Parameters:
    text (str): The text to analyze.
    
    Returns:
    dict: A dictionary indicating the presence and count of achievements.
    """
    achievement_keywords = ['achieved', 'accomplished', 'improved', 'increased']
    achievements = [word for word in text.split() if word in achievement_keywords]
    return {
        'has_achievements': len(achievements) > 0,
        'achievement_count': len(achievements)
    }

def analyze_language(tokens):
    """
    Analyzes the language use in the resume, including word count and uniqueness.
    
    Parameters:
    tokens (list): A list of tokens (words) from the resume.
    
    Returns:
    dict: A dictionary indicating the word count and unique word count.
    """
    return {
        'word_count': len(tokens),
        'unique_words': len(set(tokens))
    }

def analyze_keywords(text, tfidf):
    """
    Analyzes the presence of important keywords in the resume.
    
    Parameters:
    text (str): The text to analyze.
    tfidf (TfidfVectorizer): A TF-IDF vectorizer object for keyword analysis.
    
    Returns:
    list: A list of the top 5 most common words in the text.
    """
    word_freq = {}
    for word in text.split():
        if len(word) > 3:  # ignore short words
            word_freq[word] = word_freq.get(word, 0) + 1
    return sorted(word_freq, key=word_freq.get, reverse=True)[:5]

def analyze_certifications(text):
    """
    Analyzes the certifications mentioned in the resume.
    
    Parameters:
    text (str): The text to analyze.
    
    Returns:
    dict: A dictionary indicating the presence and count of certifications.
    """
    cert_keywords = ['certified', 'certification', 'certificate']
    has_certifications = any(keyword in text for keyword in cert_keywords)
    return {
        'has_certifications': has_certifications,
        'certification_count': len([word for word in text.split() if word in cert_keywords])
    }

def analyze_projects(text):
    """
    Analyzes the projects mentioned in the resume.
    
    Parameters:
    text (str): The text to analyze.
    
    Returns:
    dict: A dictionary indicating the presence and count of projects.
    """
    project_keywords = ['project', 'developed', 'built', 'created']
    has_projects = any(keyword in text for keyword in project_keywords)
    return {
        'has_projects': has_projects,
        'project_count': len([word for word in text.split() if word in project_keywords])
    }

def analyze_volunteer_experience(text):
    """
    Analyzes the volunteer experience mentioned in the resume.
    
    Parameters:
    text (str): The text to analyze.
    
    Returns:
    dict: A dictionary indicating the presence and details of volunteer experience.
    """
    volunteer_keywords = ['volunteer', 'volunteered', 'community service']
    has_volunteer_experience = any(keyword in text for keyword in volunteer_keywords)
    return {
        'has_volunteer_experience': has_volunteer_experience,
        'details': 'Volunteer experience found' if has_volunteer_experience else 'No volunteer experience section'
    }

def analyze_interests(text):
    """
    Analyzes the personal interests mentioned in the resume.
    
    Parameters:
    text (str): The text to analyze.
    
    Returns:
    dict: A dictionary indicating the presence and details of personal interests.
    """
    interest_keywords = ['interests', 'hobbies']
    has_interests = any(keyword in text for keyword in interest_keywords)
    return {
        'has_interests': has_interests,
        'details': 'Interests section found' if has_interests else 'No interests section'
    }

def analyze_references(text):
    """
    Analyzes the references mentioned in the resume.
    
    Parameters:
    text (str): The text to analyze.
    
    Returns:
    dict: A dictionary indicating the presence and details of references.
    """
    reference_keywords = ['references', 'available upon request']
    has_references = any(keyword in text for keyword in reference_keywords)
    return {
        'has_references': has_references,
        'details': 'References section found' if has_references else 'No references section'
    }

def analyze_formatting(text):
    """
    Analyzes the formatting of the resume, including bullet points and sections.
    
    Parameters:
    text (str): The text to analyze.
    
    Returns:
    dict: A dictionary indicating the presence and quality of formatting elements.
    """
    bullet_points = text.count('•')
    sections = text.count('\n\n')
    return {
        'bullet_points': bullet_points,
        'section_breaks': sections
    }

def analyze_professional_development(text):
    """
    Analyzes the professional development activities mentioned in the resume.
    
    Parameters:
    text (str): The text to analyze.
    
    Returns:
    dict: A dictionary indicating the presence and details of professional development activities.
    """
    development_keywords = ['professional development', 'training', 'workshop']
    has_development = any(keyword in text for keyword in development_keywords)
    return {
        'has_development': has_development,
        'details': 'Professional development activities found' if has_development else 'No professional development activities'
    }

def analyze_publications(text):
    """
    Analyzes the publications mentioned in the resume.
    
    Parameters:
    text (str): The text to analyze.
    
    Returns:
    dict: A dictionary indicating the presence and details of publications.
    """
    publication_keywords = ['publication', 'published', 'article', 'research']
    has_publications = any(keyword in text for keyword in publication_keywords)
    return {
        'has_publications': has_publications,
        'publication_count': len([word for word in text.split() if word in publication_keywords])
    }

def analyze_technical_skills(text):
    """
    Analyzes the technical skills mentioned in the resume.
    
    Parameters:
    text (str): The text to analyze.
    
    Returns:
    dict: A dictionary indicating the presence and details of technical skills.
    """
    tech_skills_keywords = ['programming', 'software', 'technical']
    has_technical_skills = any(keyword in text for keyword in tech_skills_keywords)
    return {
        'has_technical_skills': has_technical_skills,
        'tech_skill_count': len([word for word in text.split() if word in tech_skills_keywords])
    }

def analyze_language_proficiencies(text):
    """
    Analyzes the language proficiencies mentioned in the resume.
    
    Parameters:
    text (str): The text to analyze.
    
    Returns:
    dict: A dictionary indicating the presence and details of language proficiencies.
    """
    language_keywords = ['language', 'fluent', 'proficient', 'bilingual']
    has_language_proficiencies = any(keyword in text for keyword in language_keywords)
    return {
        'has_language_proficiencies': has_language_proficiencies,
        'language_count': len([word for word in text.split() if word in language_keywords])
    }

def analyze_online_presence(text):
    """
    Analyzes the online presence links mentioned in the resume.
    
    Parameters:
    text (str): The text to analyze.
    
    Returns:
    dict: A dictionary indicating the presence and details of online presence.
    """
    online_keywords = ['linkedin', 'github', 'portfolio']
    has_online_presence = any(keyword in text for keyword in online_keywords)
    return {
        'has_online_presence': has_online_presence,
        'details': 'Online presence found' if has_online_presence else 'No online presence links'
    }

def analyze_awards_and_honors(text):
    """
    Analyzes the awards and honors mentioned in the resume.
    
    Parameters:
    text (str): The text to analyze.
    
    Returns:
    dict: A dictionary indicating the presence and details of awards and honors.
    """
    awards_keywords = ['award', 'honor', 'recognition']
    has_awards = any(keyword in text for keyword in awards_keywords)
    return {
        'has_awards': has_awards,
        'award_count': len([word for word in text.split() if word in awards_keywords])
    }

def analyze_industry_specific_elements(text):
    """
    Analyzes industry-specific elements mentioned in the resume.
    
    Parameters:
    text (str): The text to analyze.
    
    Returns:
    dict: A dictionary indicating the presence and details of industry-specific elements.
    """
    industry_keywords = ['industry', 'sector', 'domain']
    has_industry_elements = any(keyword in text for keyword in industry_keywords)
    return {
        'has_industry_elements': has_industry_elements,
        'industry_count': len([word for word in text.split() if word in industry_keywords])
    }
    
def provide_overall_assessment(feedback):
    """
    Provides an overall assessment of the resume based on the analysis results.
    
    Parameters:
    feedback (dict): The dictionary containing analysis results.
    
    Returns:
    dict: A dictionary indicating the overall assessment and key recommendations.
    """
    overall = {
        'completeness': sum(1 for key, value in feedback.items() if isinstance(value, dict) and value.get('exists', False)) >= 10,
        'quality': 'good' if isinstance(feedback.get('structure'), dict) and feedback.get('structure', {}).get('well_structured', False) else 'needs improvement',
        'recommendations': 'Consider enhancing your summary, education, and work experience sections.'
    }
    return overall

# Chargement des e-mails envoyés depuis le fichier JSON
def load_sent_emails():
    if os.path.exists(SENT_EMAILS_FILE):
        with open(SENT_EMAILS_FILE, 'r') as file:
            return json.load(file)
    return {}  # Default to empty if file does not exist

# Sauvegarde des e-mails envoyés dans le fichier JSON
def save_sent_emails(sent_emails):
    with open(SENT_EMAILS_FILE, 'w') as file:
        json.dump(sent_emails, file, indent=4)

# Chargement des questions depuis le fichier JSON
def load_questions():
    if os.path.exists(QUESTIONS_FILE):
        with open(QUESTIONS_FILE, 'r') as file:
            data = json.load(file)
            next_id = max(map(int, data.keys()), default=0) + 1
            return data, next_id
    return {}, 1  # Default to 1 if no questions exist

# Sauvegarde des questions dans le fichier JSON
def save_questions(questions):
    with open(QUESTIONS_FILE, 'w') as file:
        json.dump(questions, file, indent=4)

# Vérifie si l'utilisateur est un administrateur
def is_admin(update: Update) -> bool:
    return update.message.from_user.id in admin_user_ids

# Chargement des questions et définition de l'ID suivant
questions, next_id = load_questions()
# Chargement des e-mails envoyés
sent_emails = load_sent_emails()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('👋 Bonjour ! Utilisez /question pour poser une question, /liste_questions pour voir et répondre aux questions (réservé aux administrateurs), ou /sendcv pour recevoir un CV. 📄')

async def ask_question(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global next_id
    if len(context.args) == 0:
        await update.message.reply_text('❗ Veuillez fournir votre question.')
        return

    question_text = ' '.join(context.args)
    user_id = update.message.from_user.id

    # Stocker la question avec un ID incrémental
    questions[next_id] = {
        'user_id': user_id,
        'question': question_text,
        'answered': False
    }

    # Mise à jour du prochain ID
    next_id += 1
    
    # Sauvegarde des questions
    save_questions(questions)

    await update.message.reply_text('✅ Votre question a été soumise et sera répondue par un administrateur. 🙏')

async def liste_questions(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not is_admin(update):
        await update.message.reply_text('🚫 Vous n\'êtes pas autorisé à utiliser cette commande.')
        return

    if len(context.args) == 0:
        # Afficher les questions non répondues
        unanswered_questions = [f'❓ ID: {qid}, Question: {q["question"]}' for qid, q in questions.items() if not q['answered']]

        if not unanswered_questions:
            await update.message.reply_text('🟢 Aucune question non répondue.')
        else:
            await update.message.reply_text('\n'.join(unanswered_questions))
    else:
        # Traiter la réponse à une question
        if len(context.args) < 2:
            await update.message.reply_text('❗ Veuillez fournir l\'ID de la question et la réponse.')
            return

        question_id = int(context.args[0])
        answer_text = ' '.join(context.args[1:])

        if question_id not in questions or questions[question_id]['answered']:
            await update.message.reply_text('❌ La question n\'existe pas ou a déjà été répondue.')
            return

        # Stocker la réponse
        questions[question_id]['answer'] = answer_text
        questions[question_id]['answered'] = True

        # Sauvegarde des questions
        save_questions(questions)

        await update.message.reply_text(f'✅ La question ID {question_id} a été répondue. ✍️')


async def send_cv(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Check if the message is from the correct topic
    topic_id = 3137
    if update.message.message_thread_id != topic_id:
        await update.message.reply_text('🚫 Cette commande est restreinte au topic CV_UP إحصل على نموذج السيرة')
        return
    
    # Join all arguments into a single string
    full_input = ' '.join(context.args)

    # Check if the command has at least one argument
    if not full_input:
        await update.message.reply_text(
            '❌ Format de commande incorrect. Utilisez :\n'
            '/sendcv [email], [junior|senior]\n\n'
            'Exemple : /sendcv email@gmail.com, junior\n'
            '👉 Assurez-vous d\'inclure une virgule entre l\'email et le type de CV.'
        )
        return

    # Split the input string by comma and strip surrounding spaces
    try:
        email, cv_type = map(str.strip, full_input.split(','))
    except ValueError:
        await update.message.reply_text(
            '❌ Format d\'argument invalide. Utilisez :\n'
            '/sendcv [email], [junior|senior]\n\n'
            'Exemple : /sendcv email@gmail.com, junior\n'
            '👉 Vérifiez que vous avez inclus une virgule entre l\'email et le type de CV.'
        )
        return

    # Improved email regex pattern
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(?:\.[a-zA-Z]{2,})?$'

    # Check for valid email format
    if not re.match(email_regex, email):
        await update.message.reply_text(
            '❌ Format d\'email invalide. Veuillez fournir un email valide.\n'
            'Exemple : email@gmail.com\n'
            '👉 Vérifiez que l\'adresse email ne contient pas d\'espaces supplémentaires ou de caractères invalides.'
        )
        return

    # Normalize cv_type input (lowercase)
    cv_type = cv_type.lower()  # Convert to lowercase for consistency
    if cv_type not in CV_FILES:
        await update.message.reply_text(
            '❌ Type de CV incorrect. Veuillez utiliser "junior" ou "senior".\n'
            'Exemples :\n'
            '/sendcv email@gmail.com, junior\n'
            '/sendcv email@gmail.com, senior\n'
            '👉 Vérifiez l\'orthographe et assurez-vous de ne pas utiliser d\'espaces supplémentaires.'
        )
        return

    # Check if the email has already received a CV
    if email in sent_emails:
        await update.message.reply_text(
            '📩 Vous êtes limités à un seul type de CV. 🚫'
        )
        return

    # Check if the CV file exists
    if not os.path.exists(CV_FILES[cv_type]):
        await update.message.reply_text('❌ Le fichier CV n\'existe pas. Veuillez vérifier le type de CV.')
        return

    # Remaining code for sending the CV...
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = email
        msg['Subject'] = f'{cv_type.capitalize()} CV'

        part = MIMEBase('application', 'octet-stream')
        with open(CV_FILES[cv_type], 'rb') as file:
            part.set_payload(file.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename={cv_type}_cv.docx')
        msg.attach(part)

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, email, msg.as_string())

        # Update the sent emails dictionary and save to file
        sent_emails[email] = cv_type
        save_sent_emails(sent_emails)

        await update.message.reply_text(
           f'✅ Le CV de type {cv_type.capitalize()} a été envoyé à {email}. ✉️\n\n'
           'سعداء جدا باهتمامكم بمبادرة CV_UP ! 🌟\n\n'
           'لقد تحصلتم على نسخة من مودال CV_UP التي ستساعدكم في تفادي أغلب الأخطاء التي قد تحرمكم من فرص العمل. 📝\n\n'
           'بقي الآن تعديلها وفقًا لمعلوماتكم. ✍️\n\n'
           '📄 ملاحظة: لا تنسوا دفع ثمن السيرة الذاتية إما بالتبرع بالدم في إحدى المستشفيات 🩸 أو التبرع بمبلغ من المال إلى جمعية البركة الجزائرية 💵، الذين بدورهم يوصلون التبرعات إلى غزة. 🙏\n\n'
           ' نرجو منكم تأكيد تسديد ثمن النسخة والذي كان التبرع بالدم في أحد المستشفيات أو التبرع لغزة عن طريق جمعية البركة. على الحساب   التالي CCP. 210 243 29 Clé 40 🏥✊'
        )

    except Exception as e:
        logging.error(f'Erreur lors de l\'envoi de l\'e-mail : {e}')
        await update.message.reply_text('❌ Erreur lors de l\'envoi de l\'e-mail. Veuillez réessayer.')

async def my_id(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    await update.message.reply_text(f'🔍 Votre ID est : {user_id}')



interacted_users = {}

# Update this list with users who interact with the bot
def track_user(update: Update) -> None:
    user_id = update.message.from_user.id
    chat_id = update.effective_chat.id

    if chat_id not in interacted_users:
        interacted_users[chat_id] = set()

    interacted_users[chat_id].add(user_id)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    track_user(update) 



  
    


async def tag_all(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not is_admin(update):
        await update.message.reply_text('🚫 Vous n\'êtes pas autorisé à utiliser cette commande.')
        return

    if not context.args:
        await update.message.reply_text('❗ Veuillez fournir un message à envoyer.')
        return

    message = ' '.join(context.args)
    chat_id = update.effective_chat.id

    if chat_id not in interacted_users:
        await update.message.reply_text('❗ Aucun utilisateur à taguer trouvé.')
        return

    user_ids = list(interacted_users[chat_id])
    member_tags = [f'[{user_id}](tg://user?id={user_id})' for user_id in user_ids]

    try:
        # Split the members into groups to avoid hitting message length limits
        for i in range(0, len(member_tags), 5):
            group = member_tags[i:i+5]
            await context.bot.send_message(
                chat_id=chat_id,
                text=f"{message}\n\n{' '.join(group)}",
                parse_mode='Markdown'
            )
            # Add a small delay to avoid hitting rate limits
            await asyncio.sleep(1)
        
        await update.message.reply_text('✅ Tous les membres ont été tagués avec succès.')
    except Exception as e:
        await update.message.reply_text(f'❌ Une erreur s\'est produite : {str(e)}')



async def welcome_new_member(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    for new_member in update.message.new_chat_members:
        await update.message.reply_text(
            f"Welcome {new_member.mention_html()}! 👋\n\n"
            "🌟 CV_UP is an initiative aimed at assisting Algerian youth in securing job positions by helping them design their CVs and prepare for job interviews. 📄💼\n\n"
            "Here's our group policy:\n"
            "1. Be respectful to all members. 🤝\n"
            "2. No spam or self-promotion. 🚫\n"
            "3. Use the commands below to interact with the bot. 🤖\n\n"
            "Available commands:\n"
            "/start - Get started with the bot\n"
            "/question [your question] - Ask a question (e.g., /question How do I improve my CV?)\n"
            "/sendcv [email], [junior|senior] - Request a CV (e.g., /sendcv email@example.com, junior)\n"
            "/myid - Get your Telegram user ID\n\n"
            "Enjoy your stay! 😊\n\n"
            "--------------------\n\n"
            f"مرحبًا {new_member.mention_html()}! 👋\n\n"
            "🌟 مبادرة CV_UP هي مبادرة تهدف لمرافقة الشباب الجزائري للحصول على مناصب شغل بمساعدتهم في تصميم السير الذاتية و تحضير مقابلات العمل. 📄💼\n\n"
            "إليك سياسة مجموعتنا:\n"
            "١. احترم جميع الأعضاء. 🤝\n"
            "٢. ممنوع الرسائل غير المرغوب فيها أو الترويج الذاتي. 🚫\n"
            "٣. استخدم الأوامر أدناه للتفاعل مع البوت. 🤖\n\n"
            "الأوامر المتاحة:\n"
            "/start - ابدأ استخدام البوت\n"
            "/question [سؤالك] - اطرح سؤالاً (مثال: /question كيف يمكنني تحسين سيرتي الذاتية؟)\n"
            "/sendcv [البريد الإلكتروني], [junior|senior] - اطلب سيرة ذاتية (مثال: /sendcv email@example.com, junior)\n"
            "/myid - احصل على معرف المستخدم الخاص بك على تيليجرام\n\n"
            "نتمنى لك إقامة طيبة! 😊",
            parse_mode='HTML'
        )
        
async def start_p(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    await update.message.reply_text('Welcome to the Resume Analyzer Bot! Send me a resume file (.docx or .pdf) to analyze.')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text('Upload a .docx or .pdf file of a resume, and I will analyze it for you!')
    
async def analyze_cv(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Analyze the uploaded resume file."""
    if not update.message.document:
        await update.message.reply_text('Please upload a .docx or .pdf file to analyze.')
        return

    file = await context.bot.get_file(update.message.document.file_id)
    file_name = update.message.document.file_name

    if not (file_name.endswith('.docx') or file_name.endswith('.pdf')):
        await update.message.reply_text('Please upload a .docx or .pdf file.')
        return

    await update.message.reply_text('Analyzing your resume... Please wait.')

    # Download the file
    download_path = f"temp_{file_name}"
    await file.download_to_drive(download_path)

    try:
        # Analyze the resume
        analysis_result = analyze_resume(download_path)
        assessment = generate_resume_assessment(analysis_result)


        # Convert the analysis result to a formatted string
        formatted_result = assessment

        # Split the message if it's too long
        if len(formatted_result) > 4096:
            for i in range(0, len(formatted_result), 4096):
                await update.message.reply_text(formatted_result[i:i+4096])
        else:
            await update.message.reply_text(formatted_result)

    except Exception as e:
        await update.message.reply_text(f"An error occurred while analyzing the resume: {str(e)}")

    finally:
        # Clean up the temporary file
        if os.path.exists(download_path):
            os.remove(download_path)
            
            
# File to store scraped data

# ... (rest of your imports and configurations)

# File to store scraped data
SCRAPED_DATA_FILE = 'scraped_linkedin_data.json'

def scrape_linkedin():
    chrome_options = Options()
    # chrome_options.add_argument("--headless")  # Run in headless mode to reduce resource consumption
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    service = Service('chromedriver.exe')  # Replace with your ChromeDriver path
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        # Navigate to LinkedIn login page
        driver.get('https://www.linkedin.com/login/fr?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin')
        driver.get('https://triemploi.com/jobs')

        # # Enter email
        # email_field = WebDriverWait(driver, 10).until(
        #     EC.presence_of_element_located((By.ID, 'username'))
        # )
        # email_field.send_keys('houdachezaki@gmail.com')  # Replace with actual email

        # # Enter password
        # password_field = driver.find_element(By.ID, 'password')
        # password_field.send_keys('Astrogate2024')  # Replace with actual password

        # # Click sign in
        # sign_in_submit = driver.find_element(By.CSS_SELECTOR, '.btn__primary--large')
        # sign_in_submit.click()

        # Wait for the page to load and the profile to be accessible
   

        # Navigate to the target page
        # driver.get('https://www.linkedin.com/in/chahinez-aitbraham-439b5b1b0/recent-activity/all/')
        # WebDriverWait(driver, 20).until(
        #     EC.presence_of_element_located((By.ID, 'feed-tab-icon'))
        # )
        # Wait for the elements to be present
        elements = WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, '#myList > li > div > div.text-col > div > h4 > a'))
        )

        # Extract and return the text content of the elements
        data = [element.text.strip() for element in elements]
        return data

    except TimeoutException as e:
        print(f"Timeout occurred: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()
        
async def admin_scrape(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not is_admin(update):
        await update.message.reply_text('🚫 You are not authorized to use this command.')
        return

    chat_id = update.message.chat_id
    await context.bot.send_message(chat_id=chat_id, text='Starting LinkedIn scraping, please wait...')

    try:
        new_data = scrape_linkedin()

        if os.path.exists(SCRAPED_DATA_FILE):
            with open(SCRAPED_DATA_FILE, 'r') as file:
                existing_data = json.load(file)
        else:
            existing_data = []

        for item in new_data:
            if item not in existing_data:
                existing_data.append(item)

        with open(SCRAPED_DATA_FILE, 'w') as file:
            json.dump(existing_data, file, indent=4)

        await context.bot.send_message(chat_id=chat_id, text=f'Scraped and saved {len(new_data)} items. Total unique items: {len(existing_data)}')

    except Exception as e:
        await context.bot.send_message(chat_id=chat_id, text=f'Error during scraping: {str(e)}')



async def offremploi(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Check if the message is from the correct topic
    topic_id = 3148
    if update.message.message_thread_id != topic_id:
        await update.message.reply_text('🚫 Cette commande est restreinte au topic CV_UP عروض العمل')
        return
    
    if not is_admin(update):
        await update.message.reply_text('🚫 You are not authorized to use this command.')
        return

    chat_id = update.message.chat_id

    await update.message.reply_text('Fetching job offers, please wait...')

    try:
        if os.path.exists(SCRAPED_DATA_FILE):
            with open(SCRAPED_DATA_FILE, 'r') as file:
                data = json.load(file)
            
            if not data:
                await update.message.reply_text('No job offers found.')
            else:
                for index, text in enumerate(data):
                    message = f'Job Offer {index + 1}: {text}\n\n🔵 Les candidats intéressés, envoyez vos candidatures à l\'adresse suivante :\n📩 : candidat@triemploi.com'
                    await update.message.reply_text(message)
        else:
            await update.message.reply_text('No job offers available yet. Please wait for an admin to update the data.')

    except json.JSONDecodeError:
        logging.error(f'Error decoding JSON from {SCRAPED_DATA_FILE}')
        await update.message.reply_text('❌ Error reading job offers data. Please contact an administrator.')

    except Exception as e:
        logging.error(f'Unexpected error in offremploi: {e}')
        await update.message.reply_text('❌ An unexpected error occurred. Please try again later.')

def generate_resume_assessment(analysis_result):
    assessment = []
    score = 0
    max_score = 0

    essential_sections = ['contact_info', 'summary', 'education', 'work_experience', 'skills']
    for section in essential_sections:
        max_score += 1
        if analysis_result.get(section, {}).get('exists', False):
            score += 1
            assessment.append(f"✅ Your resume includes a {section.replace('_', ' ')} section.")
        else:
            assessment.append(f"❌ Your resume is missing a {section.replace('_', ' ')} section.")

    valuable_sections = ['achievements', 'projects', 'certifications', 'volunteer_experience']
    for section in valuable_sections:
        max_score += 0.5
        if analysis_result.get(section, {}).get(f'has_{section}', False):
            score += 0.5
            assessment.append(f"👍 Good job including {section.replace('_', ' ')} in your resume.")
        else:
            assessment.append(f"💡 Consider adding a {section.replace('_', ' ')} section to strengthen your resume.")

    max_score += 1
    if 'keywords' in analysis_result and len(analysis_result['keywords']) >= 5:
        score += 1
        assessment.append("✅ Your resume includes relevant keywords.")
    else:
        assessment.append("❌ Your resume could use more industry-specific keywords.")

    max_score += 1
    if analysis_result.get('structure', {}).get('well_structured', False):
        score += 1
        assessment.append("✅ Your resume has a good overall structure.")
    else:
        assessment.append("❌ The structure of your resume could be improved.")

    percentage_score = (score / max_score) * 100

    if percentage_score >= 90:
        overall = "Excellent! Your resume is very strong."
    elif percentage_score >= 70:
        overall = "Good job! Your resume is solid but has room for improvement."
    elif percentage_score >= 50:
        overall = "Your resume needs some work to stand out to employers."
    else:
        overall = "Your resume needs significant improvements to be competitive."

    assessment.append(f"\n📊 Overall Score: {percentage_score:.1f}%")
    assessment.append(f"💬 {overall}")
    assessment.append("\nKey Recommendations:")
    
    if 'summary' not in analysis_result or not analysis_result['summary'].get('exists', False):
        assessment.append("- Add a strong summary statement to quickly highlight your qualifications.")
    if 'achievements' not in analysis_result or not analysis_result['achievements'].get('has_achievements', False):
        assessment.append("- Include specific achievements to demonstrate your impact in previous roles.")
    if 'skills' not in analysis_result or not analysis_result['skills'].get('exists', False):
        assessment.append("- Create a dedicated skills section to showcase your key competencies.")

    return "\n".join(assessment)


def main():
    # Configuration des logs²
    logging.basicConfig(level=logging.INFO)

    # Création de l'application et passage du token du bot
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Ajout des gestionnaires de commandes
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("question", ask_question))
    app.add_handler(CommandHandler("liste_questions", liste_questions))
    app.add_handler(CommandHandler("sendcv", send_cv))
    app.add_handler(CommandHandler("myid", my_id))
    # Add the admin scrape command handler
    app.add_handler(CommandHandler("admin_scrape", admin_scrape))

    # Add the offremploi command handler
    app.add_handler(CommandHandler("offremploi", offremploi))    # Add this line to your main() function to register the new command
    app.add_handler(CommandHandler("tagall", tag_all))
     # Register command handlers
    app.add_handler(CommandHandler("start_p", start_p))
    app.add_handler(CommandHandler("help", help_command))
    # app.add_handler(CommandHandler("analyze_cv", analyze_cv))
    # Add handler for new chat members
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome_new_member))
    # app.add_handler(MessageHandler(filters.Document, analyze_cv))
    # app.add_handler(MessageHandler(filters.ATTACHMENT & filters.Document.ALL, analyze_cv))


    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    return application

    # Démarrage de l'application
    # app.run_polling()

# Webhook handler
async def webhook(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await main().process_update(update)

if __name__ == '__main__':
    file_path = "my_telegram_bot/CV Projects Sales Manager, Mr BAHI Takieddine.pdf"  # Replace with your file path

     # Analyze the resume
    # analysis_result_p = analyze_resume(file_path)
    
    # Generate the assessment
    # assessment = generate_resume_assessment(analysis_result_p)
    
    # print(assessment)  # Print the assessment directly
    
    main()