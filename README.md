# RedditSavedImagesGrabber
Grabs saved Images from reddit, saves and logs them


## 1. Create Reddit App and fill Credentials
Follow the Tutorial here to get an App Client ID and App Client Secret:
https://github.com/reddit-archive/reddit/wiki/OAuth2-Quick-Start-Example

## 2 Create Folder Structure
For the script to work properly you need to create a "logs.txt" file and an "savedImages" Folder

Place both of them inside a folder together with LinkLookup.py and Scrubber.py

## 3 Run Script
Run the Script, it should output which images are being downloaded, and log them to logs.txt

Parameters can be passed as following: LinkLookup.py [Username] [AppID] [AppSecret]

It also unsaves every post it downloads

## 4 Deleting
If you delete any images inside savedImages, you can run the Scrubber.py script to remove all unnecessary logs from logs.txt

