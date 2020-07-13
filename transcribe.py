#!/usr/bin/env python3

import os, sys
import requests, json

class Transcribe:
	def __init__(self,filename):
		self.filename = filename

	def identifyFormat(self):
		valid_extensions = ('.mp3','.ogg','.wav','.m4a','.flac')
		file_path, file_extension = os.path.splitext(self.filename)
		if file_extension in valid_extensions:
			# print('Valid')
			pass
		else:
			error = 'File extension ' + file_extension + ' not valid!'
			raise AssertionError(error)

	def request():
		pass

	def printResponse():
		pass


if __name__ == "__main__":
	file_name = sys.argv[1]


	obj = Transcribe(file_name)
	obj.identifyFormat()


	