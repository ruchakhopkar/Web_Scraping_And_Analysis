# Web_Scraping_And_Analysis
This project scrapes the Linkedin jobs to get location, title, company, main keywords, salary if posted and minimum qualifications.

### Skills Used
Programming Language: Python
Web Scraping using BeautifulSoup
Natural Language Processing: nltk, spacy
Supporting Libraries: numpy, pandas, regex

### Pipeline
![web scraping](https://github.com/ruchakhopkar/Web_Scraping_And_Analysis/assets/70127769/c23607f2-ac74-47a5-ab4f-29f3a3fb5f97)


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
Lets break down on how to get the individual components.
**Job Title:** 
![image](https://github.com/ruchakhopkar/Web_Scraping_And_Analysis/assets/70127769/c65872ea-6948-4af2-b82f-24015fa56846)
We see that if we can filter the 'div' tag that has a class 'base-card relative w-full hover:no-underline focus:no-underline base-card--link base-search-card base-search-card--link job-search-card', we will be able to retrieve its text which would be the job title.
These components are highlighted.

In similar ways, we will be able to get all the details of the job posting. 

