import requests
from dicttoxml import dicttoxml
from github import Github
import os

# adding connection to the .env file
from dotenv import load_dotenv
load_dotenv()


url = 'https://active-jobs-db.p.rapidapi.com/active-ats-7d'
querystring = {
    "limit": "50",
    "offset": "0",
    "title_filter": '"Software Engineer"',
    "location_filter": '"Argentina" OR "Bolivia" OR "Brazil" OR "Chile" OR "Colombia" OR "Costa Rica" OR "Cuba" OR "Dominican Republic" OR "Ecuador" OR "El Salvador" OR "Guatemala" OR "Honduras" OR "Mexico" OR "Nicaragua" OR "Panama" OR "Paraguay" OR "Peru" OR "Puerto Rico" OR "Uruguay" OR "Venezuela"',
    "description_type": "text"
}
headers = {
    'x-rapidapi-host': 'active-jobs-db.p.rapidapi.com',
    'x-rapidapi-key': os.environ.get('RAPID_API_KEY') 
}


response = requests.get(url, headers=headers, params=querystring)
response.raise_for_status()
json_data = response.json()


xml_data = dicttoxml(json_data, custom_root='jobs', attr_type=False)


xml_file_path = "job_data.xml"
with open(xml_file_path, "wb") as f:
    f.write(xml_data)
print("XML conversion done and saved locally.")


GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN')
REPO_NAME = "GeorgesJanin/xml_hosting"  
FILE_PATH_IN_REPO = "job_data.xml"      
COMMIT_MESSAGE = "Update job data XML"

g = Github(GITHUB_TOKEN)
repo = g.get_repo(REPO_NAME)

try:
    contents = repo.get_contents(FILE_PATH_IN_REPO)
    repo.update_file(
        path=contents.path,
        message=COMMIT_MESSAGE,
        content=xml_data.decode('utf-8'),
        sha=contents.sha
    )
    print("File updated in GitHub repo.")
except Exception as e:
    repo.create_file(
        path=FILE_PATH_IN_REPO,
        message=COMMIT_MESSAGE,
        content=xml_data.decode('utf-8')
    )
    print("File created in GitHub repo.")
