import requests
import json

url = "https://classroom.googleapis.com/v1/courses/764169243133/courseWork/698788015501/studentSubmissions"
headers = {"Authorization": "Bearer ya29.a0AeXRPp4HrYvO2bmzTX3dO6Vk09BSaInwyazC3GTQGyI8yTsN_oAeYAVFTo4I7eMRL6CvH_zKX6aDbcN_TebvhiNSDb4k0WO98IHV7VN63aDqOzEW1fZ4QD07qkXv543kdnjTt98kj61Do_gQibCjkxVa_CiozAWGCVW2nb2VaCgYKAeQSARMSFQHGX2MinvTkPeFOwlP7lIdA017PCw0175"}

response = requests.get(url, headers=headers)
data = response.json()

print(json.dumps(data, indent=4))
