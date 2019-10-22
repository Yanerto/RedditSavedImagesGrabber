#!/usr/bin/env python3
#Script to download all saved Images a user has
import requests
import requests.auth
import urllib.request
import sys
import os.path
import time
import getpass

#Sends query to get OAuth token
def getAuthToken(username, AppID, AppSecret, password):
	client_auth = requests.auth.HTTPBasicAuth(AppID, AppSecret)
	post_data = {"grant_type": "password", "username": "%s" % username, "password": "%s" % password}
	headers = {"User-Agent": "SavedImagesGrabber/1.1 by Yanerto"}
	token = requests.post("https://www.reddit.com/api/v1/access_token", auth=client_auth, data=post_data, headers=headers)

	return token;

def downloadPost(url, fileName):
	#Check if fileName already exists, create new Name with Timestamp if true
	if os.path.isfile(fileName):
		ts = time.time()
		fileName = "savedImages/" + str(ts) + url.split("/")[-1]

	#Download file from url
	try:
		urllib.request.urlretrieve(url, fileName)
	except urllib.error.HTTPError:
		print("File not found. Perhaps it has been deleted")

	return;

def unsavePost(id):
	post_data = {"id": id}
	print(post_data)
	reponse = requests.post("https://oauth.reddit.com/api/unsave", data=post_data, headers = headers)
	return;


print("Welcome!")

#Get Credentials of user
username = ""
AppID = ""
AppSecret = ""

if len(sys.argv) == 4:
	username = sys.argv[1]
	AppID = sys.argv[2]
	AppSecret = sys.argv[3]
	password = getpass.getpass("Password of Reddit Account: ")
else:
	username    = input("Username of Reddit Account: ")
	password    = getpass.getpass("Password of Reddit Account: ")
	AppID       = input("App Client ID: ")
	AppSecret   = input("App Secret: ")

#Get Authentication Token
token = getAuthToken(username, AppID, AppSecret, password)

#Check if password was correct, else quit script
if(len(token.json())) == 1:
	sys.exit("Wrong Password. Exiting Script")

#Get saved posts from API
headers = {"Authorization": "bearer " + token.json()['access_token'], "User-Agent": "SavedImagesGrabber/1.1 by Yanerto"}
response = requests.get("https://oauth.reddit.com/user/%s/saved" % username,headers=headers)
dataResponse = response.json()

#Iterate through Listing, save every image
upperLimit = len(dataResponse["data"]["children"])
for x in range(0,upperLimit):
    if dataResponse["data"]["children"][x]["kind"] == "t1":
        print("[%d] Comment" % (x))
        continue

    url = dataResponse["data"]["children"][x]["data"]["url"]
    #print URL, for safety purpose
    menuListing = "[%d]	" % (x) + url
    print(menuListing)
    fileName = "savedImages/" + url.split("/")[-1]
    whitelist = ['awwni.me', 'i.imgur', 'i.redd.it']
    #If post URL is in whitelist, aka if post is an image
    if any(x in url for x in whitelist):
     downloadPost(url, fileName)
     unsavePost(dataResponse["data"]["children"][x]["data"]["name"])
    else:
     print("Not in Whitelist")
