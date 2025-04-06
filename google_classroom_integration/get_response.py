import requests
import json

url = "https://classroom.googleapis.com/v1/courses/COURSE_ID/courseWork/ASSIGNMENT_ID/studentSubmissions"
headers = {"Authorization": "Bearer ACCESS_TOKEN"}

response = requests.get(url, headers=headers)
data = response.json()

print(json.dumps(data, indent=4))
