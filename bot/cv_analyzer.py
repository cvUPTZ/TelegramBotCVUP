import re
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
from nltk.tokenize import word_tokenize
from docx import Document
import fitz  # PyMuPDF for PDF reading
import json

# Download required NLTK data
nltk.download('punkt')

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
    dict: A dictionary containing the analysis results for different resume sections.
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
    email_pattern = r'/\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b/
    phone_pattern = r'/\b(\+\d{1,2}\s?)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}\b|\+\d{3}\s\d{3}\s\d{3}\s\d{3}\b/
    
    email = re.search(email_pattern, text)
    phone = re.search(phone_pattern, text)
    
    return {
        'email': email.group() if email else None,
        'phone': phone.group() if phone else None
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
    education_keywords = ['education', 'degree', 'university', 'college']
    has_education = any(keyword in text for keyword in education_keywords)
    return {
        'exists': has_education,
        'details': 'Education section found' if has_education else 'No clear education section'
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



if __name__ == "__main__":
    file_path = "my_telegram_bot/CV Projects Sales Manager, Mr BAHI Takieddine.pdf"  # Replace with your file path
    analysis_result = analyze_resume(file_path)
    print(json.dumps(analysis_result, indent=4))