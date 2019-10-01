#!/usr/bin/env python3
#Python Script to remove deleted files from logs
import os

#Get List of all saved files
files = os.listdir("savedImages")

#Get List of all items in log list
with open("logs.txt", "r") as f:
	lines = f.readlines()




with open("logs.txt", "w") as f:
	for file in files:
		for line in lines:
			if file == line.split(" ")[0]:
				f.write(line)
