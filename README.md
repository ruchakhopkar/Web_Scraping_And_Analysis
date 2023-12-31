# Web_Scraping_And_Analysis
This project scrapes the Linkedin jobs to get location, title, company, main keywords, salary if posted and minimum qualifications.

### Skills Used
Programming Language: Python
Web Scraping using BeautifulSoup
Natural Language Processing: nltk, spacy
Supporting Libraries: numpy, pandas, regex

### Pipeline
![web scraping (1)](https://github.com/ruchakhopkar/Web_Scraping_And_Analysis/assets/70127769/7324dfcc-61ff-487a-a52f-34952a7cbde7)



### Description
We have a class called FindJobs that will scrap the linkedIn job posting for various parameters and append it as a row in a dataframe. 
It will scrap the following data:
1. Date of Posting
2. Job Title
3. Company Name
4. Company Website
5. Location of the job
6. Link to apply for the job
7. Keywords in the job description
8. Minimum education requirements

### Example
Lets break down on how to get the individual components.<br>
**Job Title:** 
![image](https://github.com/ruchakhopkar/Web_Scraping_And_Analysis/assets/70127769/c65872ea-6948-4af2-b82f-24015fa56846)
We see that if we can filter by the <br>
tag: **div** <br>
class: **base-card relative w-full hover:no-underline focus:no-underline base-card--link base-search-card base-search-card--link job-search-card** <br>
We will be able to retrieve its text which would be the job title.
These components are highlighted in the image.

Similarly, we get the other features like the Date of Posting, Job Title, Company Name, Company Website, Location of the job, Link to apply for the job by filtering the html content. <br><br>

To get the minimum educational requirements and the keywords in the job description, we would have to extract the contents of the job link. Therefore, we make a new object of BeautifulSoup and open the job link with it. The process will remain similar to before to extract the job description and minimum educational requirements. <br> <br>

**Extracting keywords from Job Description:**
The job description is usually mentioned as a paragraph. <br>
We want to be able to extract useful keywords from this paragraph. For this purpose, we use the spaCy model for English Language Processing. It contains pre-trained components for tokenization, part-of-speech tagging, dependency parsing, and named entity recognition. We send the job description text from this spaCy model which would return information about each token. We then subset the tokens by checking if the token is a noun and it has a verb that it depends on. We then do a second check to see if the token is present in the 'Responsibilities', 'Qualifications' or 'Skills' section or are present in the common_job_skills required by a Data Scientist.
<br>
<br>

![skills](https://github.com/ruchakhopkar/Web_Scraping_And_Analysis/assets/70127769/0a50054a-b851-4fcf-aadf-cecc1cf38da9)

We see most of the jobs include keywords like work experience, backgrounds(referring to knowledge diversity), data and technology,deadlines(ability to meet deadlines), model, frameworks and training(referring to Machine Learning skills) amongst many more. 
![company_bar_plot](https://github.com/ruchakhopkar/Web_Scraping_And_Analysis/assets/70127769/2aa3761b-3935-4c88-9663-01fc2ecb7e3e)
We see a lot of openings from the companies 'All Things Monadnock' and 'Pattern Learning AI'. 
### Conclusion:
This project might help a person looking for jobs to check and analyze their skills and the current job market. They might also extend this project to directly apply to the jobs through the job links.
