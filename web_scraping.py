
#import required libraries

from bs4 import BeautifulSoup
import requests
import json
from nltk.corpus import stopwords
import nltk
import pandas as pd
import spacy
import time
nltk.download('stopwords')
cachedStopWords = stopwords.words("english")

def extract_job_skills(job_description):
  """
  This function will get the main keywords from a job description.

  Input:
  job_description: dtype: str
                  The job description as posted.

  Returns:
  List of keywords.
  """

  # Load the spaCy model.
  nlp = spacy.load('en_core_web_sm')

  # Tokenize and tag the job description.
  doc = nlp(job_description)

  # Extract all job skills from the job description.
  job_skills = []
  for token in doc:
    if token.pos_ == 'NOUN' and token.head.pos_ == 'VERB':
        if is_job_skill(token, job_description):
            job_skills.append(token.text)

  # Return the list of job skills.
  return list(set(job_skills))

def is_job_skill(token, job_description):
  """Returns True if the given token is a job skill, False otherwise.

  Args:
    token: A spaCy token.
    job_description: A string containing the job description.

  Returns:
    A boolean indicating whether the given token is a job skill.
  """

  # Check if the token is mentioned in the "Responsibilities" section of the job description.
  if "Responsibilities" in job_description:
    responsibilities_section = job_description[job_description.find("Responsibilities") + len("Responsibilities"):]
    if token.text in responsibilities_section:
      return True

  # Check if the token is mentioned in the "Qualifications" section of the job description.
  if "Qualifications" in job_description:
    qualifications_section = job_description[job_description.find("Qualifications") + len("Qualifications"):]
    if token.text in qualifications_section:
      return True

  # Check if the token is mentioned in the "Skills" section of the job description.
  if "Skills" in job_description:
    skills_section = job_description[job_description.find("Skills") + len("Skills"):]
    if token.text in skills_section:
      return True

  # Check if the token is a common job skill.
  common_job_skills = ['Python', 'R', 'SQL', 'linear algebra', 'calculus', 'probability', 'statistics', \
                       'supervised learning', 'unsupervised learning', 'reinforcement learning', 'machine learning', \
                       'Matplotlib', 'Seaborn', 'Tableau', 'Power BI', 'Pandas', 'NumPy', 'Spark', \
                       'A/B testing', 'statistical significance testing', \
                       'ability to communicate complex technical concepts to both technical and non-technical audiences', \
                       'AWS', 'Azure', 'GCP', 'Hadoop', 'Spark', 'Hive', 'Kafka', 'Natural language processing', \
                       'Computer vision']
  if token.text in common_job_skills:
      return True

  # Otherwise, the token is not a job skill.
  return False


class FindJobs:
  def __init__(self, input_link):
      '''
      This is a constructor for finding jobs

      Parameters:
      ----------------------------------------------
      input_link: str
                  The link to the linkedin jobs page

      Returns:
      ----------------------------------------------
      None
      '''
      self.input_link = input_link

      #get the HTML content from the input link
      self.content = requests.get(self.input_link).text

  def get_date_posted(self, job, entry):
      '''
      This function will get the date when the job was posted by finding the tag 'time'.

      Parameters:
      ----------------------------------------------
      job: str
           The link to the linkedin jobs page
      entry: dictionary
            Dictionary to store all the features
      Returns:
      ----------------------------------------------
      entry: dictionary
            Updated Dictionary to store all the features
      '''
      date_posted = job.find('time')
      date_posted = ' '.join(date_posted.text.split())
      entry['Date of Posting'] = date_posted
      return entry

  def get_job_title(self, job, entry):
      '''
      This function will get the job title by finding the div tag with a specific class.

      Parameters:
      ----------------------------------------------
      job: str
           The link to the linkedin jobs page
      entry: dictionary
            Dictionary to store all the features

      Returns:
      ----------------------------------------------
      entry: dictionary
            Updated Dictionary to store all the features
      '''
      all_postings = job.find('a', {'class': "base-card__full-link absolute top-0 right-0 bottom-0 left-0 p-0 z-[2]"})
      job_title = ' '.join(all_postings.text.split())
      entry['Title'] = job_title
      return entry

  def get_company_details(self, job, entry):
      '''
      This function will get the company name and website by finding the a tag with a
      specific class.

      Parameters:
      ----------------------------------------------
      job: str
           The link to the linkedin jobs page
      entry: dictionary
            Dictionary to store all the features

      Returns:
      ----------------------------------------------
      entry: dictionary
            Updated Dictionary to store all the features
      '''
      company = job.find('a', {'class': 'hidden-nested-link'})
      company_name = ' '.join(company.text.split())
      company_website = company['href']
      entry['Company Name'] = company_name
      entry['Company Website'] = company_website
      return entry

  def get_location(self, job, entry):
      '''
      This function will get the job location by finding the div tag with a specific class.

      Parameters:
      ----------------------------------------------
      job: str
           The link to the linkedin jobs page
      entry: dictionary
            Dictionary to store all the features

      Returns:
      ----------------------------------------------
      entry: dictionary
            Updated Dictionary to store all the features
      '''
      location = job.find('div', {'class':"base-search-card__metadata"})
      location = ' '.join(location.text.split())
      entry['Location'] = location
      return entry

  def get_job_link(self, job, entry):
      '''
      This function will get the job link by finding the a tag with a specific class.

      Parameters:
      ----------------------------------------------
      job: str
           The link to the linkedin jobs page
      entry: dictionary
            Dictionary to store all the features

      Returns:
      ----------------------------------------------
      entry: dictionary
            Updated Dictionary to store all the features
      '''
      job_link = job.find('a', {'class': 'base-card__full-link absolute top-0 right-0 bottom-0 left-0 p-0 z-[2]'})['href']
      entry['Job Link'] = job_link
      return job_link

  def get_keywords(self, job_link, entry):
      '''
      This function will get the job title by finding the div tag with a specific class.

      Parameters:
      ----------------------------------------------
      job_link: str
           The link to the linkedin job
      entry: dictionary
            Dictionary to store all the features

      Returns:
      ----------------------------------------------
      entry: dictionary
            Updated Dictionary to store all the features
      '''
      #get the content from the job link
      job_description_soup = BeautifulSoup(requests.get(job_link).text, 'lxml')
      #filter the job description based on the script tag and a specified type and
      #load the data in a json file
      jd = json.loads(job_description_soup.find('script', {'type': 'application/ld+json'}).text)

      # Filter the description from the jd
      jd_skills = jd['description']
      x = jd_skills.split(';')
      #There were a lot of futile characters which needed to be eliminated.
      #The following 2 lines removes these futile characters
      x = [i for i in x if ' ' in i]
      x = ''.join([i.split('&')[0] for i in x])
      #Remove stopwords
      x = [word for word in x.split() if word not in cachedStopWords]
      #use spaCy to extract keywords as a list
      highest_occuring_words = extract_job_skills(' '.join(x))
      #save the keywords
      entry['Skills Required Keywords'] = highest_occuring_words

      #Filter the education from the jd
      jd_education = jd['educationRequirements']['credentialCategory']
      entry['Education'] = jd_education
      return entry


  def get_all_jobs(self):
      #parse the content data using Beautiful Soup
      soup = BeautifulSoup(self.content, 'lxml')
      #get all the jobs currently posted
      all_jobs = soup.find_all('div', {'class': 'base-card relative w-full hover:no-underline focus:no-underline base-card--link base-search-card base-search-card--link job-search-card'})
      #create a dataframe to store all the results
      df = pd.DataFrame()

      for job in all_jobs:
          #get all the features of the job posting
          try:
              print(job)
              entry = {}
              entry = self.get_date_posted(job, entry)
              entry = self.get_job_title(job, entry)
              entry = self.get_company_details(job, entry)
              entry = self.get_job_link(job, entry)
              entry = self.get_keywords(entry['Job Link'], entry)
              entry = pd.DataFrame(entry, index = [0])
              df = pd.concat([df, entry], axis = 0, ignore_index = True)
              break
          except:
            pass

      return df

findjobs = FindJobs('https://www.linkedin.com/jobs/search/?currentJobId=3703705492&distance=25&f_TPR=r604800&geoId=105080838&keywords=data%20science&origin=JOB_SEARCH_PAGE_JOB_FILTER')


df = findjobs.get_all_jobs()

