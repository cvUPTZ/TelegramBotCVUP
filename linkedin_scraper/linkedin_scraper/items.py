import scrapy

class LinkedInProfileItem(scrapy.Item):
    name = scrapy.Field()
    title = scrapy.Field()
    location = scrapy.Field()
    url = scrapy.Field()
    about = scrapy.Field()
    experience = scrapy.Field()
    education = scrapy.Field()
    skills = scrapy.Field()
    certifications = scrapy.Field()
    languages = scrapy.Field()
    volunteering = scrapy.Field()
    recommendations = scrapy.Field()
    accomplishments = scrapy.Field()
    interests = scrapy.Field()

class ExperienceItem(scrapy.Item):
    title = scrapy.Field()
    company = scrapy.Field()
    duration = scrapy.Field()
    location = scrapy.Field()
    description = scrapy.Field()

class EducationItem(scrapy.Item):
    school = scrapy.Field()
    degree = scrapy.Field()
    field_of_study = scrapy.Field()
    date_range = scrapy.Field()

class CertificationItem(scrapy.Item):
    name = scrapy.Field()
    issuer = scrapy.Field()
    date = scrapy.Field()

class VolunteeringItem(scrapy.Item):
    role = scrapy.Field()
    organization = scrapy.Field()
    date_range = scrapy.Field()

class RecommendationItem(scrapy.Item):
    recommender = scrapy.Field()
    relationship = scrapy.Field()
    text = scrapy.Field()