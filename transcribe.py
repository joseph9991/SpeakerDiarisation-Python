#!/usr/bin/env python3

import os, sys
import requests, json

class Transcribe:
	def __init__(self,filename):
		self.filename = filename

	# Validates the file, checks for the valid file extension and returns audio-format
	def identifyFormat(self):
		valid_extensions = ('.mp3','.ogg','.wav','.m4a','.flac')
		file_path, file_extension = os.path.splitext(self.filename)
		if file_extension in valid_extensions:
			return file_extension[1:]
		elif not file_extension:
			error = file_name + file_extension + ' is either a directory or not a valid file'
			raise AssertionError(error)
		else:
			error = 'File extension ' + file_extension + ' not valid'
			raise AssertionError(error)

	def request():
		pass

	def printResponse():
		pass


if __name__ == "__main__":
	file_name = sys.argv[1]


	obj = Transcribe(file_name)
	
	audio_format = obj.identifyFormat()
	print(audio_format)
	#response = obj.request(audio_format)

	#obj.printResponse(response)



	