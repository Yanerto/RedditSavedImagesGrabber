#!/usr/bin/env python3
#Script to download all saved Images a user has
import requests
import requests.auth
import urllib.request
import sys
import os.path
import time
import getpass

#Define variables
saveFolder = "savedImages/"
logFile = "logs.txt"
unsaveWhenDownload = False

#Sends query to get OAuth token
def getAuthToken(username, AppID, AppSecret, password):
	client_auth = requests.auth.HTTPBasicAuth(AppID, AppSecret)
	post_data = {"grant_type": "password", "username": "%s" % username, "password": "%s" % password}
	headerAuth = {"User-Agent": "SavedImagesGrabber/1.2 by Yanerto"}
	token = requests.post("https://www.reddit.com/api/v1/access_token", auth=client_auth, data=post_data, headers=headerAuth)
	return token;

#Downloads image from url and saves as fileName
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

#Removes the post with given id from saved posts
def unsavePost(id):
	post_data = {"id": id}
	reponse = requests.post("https://oauth.reddit.com/api/unsave", data=post_data, headers = header)
	return;

#Saves all posts of page with given listingVariable
def savePage(listingVariable):
	#Query Reddit API
	if(!unsaveWhenDownload):
		post_data = {"after": listingVariable}
	response = requests.get("https://oauth.reddit.com/user/%s/saved" % username, headers=header, params=post_data)
	dataResponse = response.json()
	upperLimit = len(dataResponse["data"]["children"])

	#Iterate through page, save every image
	for x in range(0, int(upperLimit)):
		if dataResponse["data"]["children"][x]["kind"] == "t1":
			print("[%d] Comment" % (x))
			continue

		url = dataResponse["data"]["children"][x]["data"]["url"]
		menuListing = "[%d]  " % (x) + url
		print(menuListing)
		fileName = "savedImages/" + url.split("/")[-1]
		whitelist = ['awwni.me', 'i.imgur', 'i.redd.it', 'media.giphy', 'cdn.discordapp']

		#If post URL is in whitelist, aka if post is an image
		if any(x in url for x in whitelist):
			downloadPost(url,fileName)
			#Log Post to text file
			with open("logs.txt", "a") as myFile:
				textToAttach = fileName[12:] + "                               " + "https://old.reddit.com" + dataResponse["data"]["children"][x]["data"]["permalink"] + " \n"
				myFile.write(textToAttach)
				if(unsaveWhenDownload):
					unsavePost(dataResponse["data"]["children"][x]["data"]["name"])
		else:
			print("Not in Whitelist")

	return dataResponse["data"]["after"];


def printMainMenu():
	print(30*"=","MENU",33*"=")
	print("1. Run")
	print("2. Options")
	print("3. Exit")
	print(69*"=")
	return;

def OptionMenu():
	global saveFolder
	global logFile
	global unsaveWhenDownload
	print(30*"=","Options",30*"=")
	print("1. Change current save Location: %s" % (saveFolder))
	print("2. Change current log File: %s" % (logFile))
	print("3. Unsave Posts when downloading?: %s" % (str(unsaveWhenDownload)) )
	print("4. Back")
	print(69*"=")

	option = getUserInput("")
	if option == 1:
		tmp = input("Please put in relative Path to folder")
		if(os.path.exists(tmp) and os.path.isdir(tmp)):
			saveFolder = tmp
		else:
			print("Given path is not correct")
	elif option == 2:
		tmp = input("Please put in the relative Path to the log file")
		if(os.path.exists(tmp)):
			logFile = tmp
		else:
			print("Given path is not correct")
	elif option == 3:
		if(unsaveWhenDownload):
			print("Saved posts will not be unsaved when downloading")
			unsaveWhenDownload = False
		else:
			print("Saved posts will be unsaved when downloading")
			unsaveWhenDownload = True
	elif option == 4:
		return;



def getUserInput(prompt):
	tmp = -1
	while tmp == -1:
		tmp = input(prompt)
	option = int(tmp)
	return option;


while 1:
	printMainMenu()
	option = getUserInput("")
	if option == 1:
		print("Run")
		break;
	elif option == 2:
		OptionMenu()
	elif option == 3:
		sys.exit("Quitting")



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


#Ask for pages
maxPages = input("How many pages to save?")
listingVariable = ""
print(token.json())
header = {"Authorization": "bearer " + token.json()['access_token'], "User-Agent": "SavedImagesGrabber/1.0 by Yanerto"}

for k in range(0, int(maxPages)):
    print(k)
    listingVariable = savePage(listingVariable)
