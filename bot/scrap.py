# from linkedin_scraper import Person, actions
# from selenium import webdriver
# driver = webdriver.Chrome()

# email = "houdachezaki@gmail.com"
# password = "Astrogate2024"
# actions.login(driver, email, password) # if email and password isnt given, it'll prompt in terminal
# person = Person("https://www.linkedin.com/in/mahfoud-ziane-26b01581/", driver=driver)



from linkedin_scraper import Person, actions
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Set up Chrome options
chrome_options = Options()
# chrome_options.add_argument("--headless")  # Run in headless mode (no browser UI)
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Initialize the Chrome driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

email = "houdachezaki@gmail.com"
password = "Astrogate2024"

# Log in to LinkedIn
actions.login(driver, email, password)

# Your LinkedIn profile URL
profile_url = "https://www.linkedin.com/in/mahfoud-ziane-26b01581/"

# Create a Person object for your profile
person = Person(profile_url, driver=driver)

# Scrape the profile
person.scrape(close_on_complete=True)

# Extract the required information
skills = person.skills  # List of skills
education = person.educations  # List of educations
experience = person.experiences  # List of experiences

# Print the extracted information
print("Skills:")
for skill in skills:
    print(f"- {skill.name}")

print("\nEducation:")
for edu in education:
    print(f"- {edu.degree} in {edu.field_of_study} from {edu.school_name} (Graduated: {edu.graduation_year})")

print("\nExperience:")
for exp in experience:
    print(f"- {exp.job_title} at {exp.company_name} (From: {exp.start_date}, To: {exp.end_date})")

# Close the browser
driver.quit()
