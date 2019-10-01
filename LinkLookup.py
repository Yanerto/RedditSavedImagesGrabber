#!/usr/bin/env python3
#Script to download all saved Images a user has
import requests
import requests.auth
import urllib.request
import sys
import os.path
import time
import getpass

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
client_auth = requests.auth.HTTPBasicAuth(AppID, AppSecret)
post_data = {"grant_type": "password", "username": "%s" % username, "password": "%s" % password}
headers = {"User-Agent": "SavedImagesGrabber/1.0 by Yanerto"}
token = requests.post("https://www.reddit.com/api/v1/access_token", auth=client_auth, data=post_data, headers=headers)

#Check if password was correct, else quit script
if(len(token.json())) == 1:
	sys.exit("Wrong Password. Exiting Script")

#Get saved posts from API
headers = {"Authorization": "bearer " + token.json()['access_token'], "User-Agent": "SavedImagesGrabber/1.0 by Yanerto"}
response = requests.get("https://oauth.reddit.com/user/%s/saved" % username,headers=headers, params=post_data)
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
    if  any(x in url for x in whitelist):

        #Check if fileName already exists, then create new fileName with timestamp
        if os.path.isfile(fileName):
            ts = time.time()
            fileName = "savedImages/" + str(ts) + url.split("/")[-1]
        #Download File
        urllib.request.urlretrieve(url, fileName)

        #Log post to image file
        with open("logs.txt", "a") as myFile:
            textToAttach = fileName[12:] + "              " + "https://old.reddit.com" + dataResponse["data"]["children"][x]["data"]["permalink"] +" \n"
            myFile.write(textToAttach)
        #Remove Post from favourites
        post_data = {"id": dataResponse["data"]["children"][x]["data"]["name"]}
        #response = requests.post("https://oauth.reddit.com/api/unsave", data=post_data, headers=headers)
    else:
        print("Not in Whitelist")
