#!/usr/bin/env python3

import os, sys
import requests, json
from requests.exceptions import HTTPError


class Transcribe:
	def __init__(self,file_name):
		self.file_name = file_name

	# Validates the file, checks for the valid file extension and returns audio-format
	def identifyFormat(self):
		valid_extensions = ('.mp3','.ogg','.wav','.m4a','.flac')
		file_path, file_extension = os.path.splitext(self.file_name)
		if file_extension in valid_extensions:
			return file_extension[1:]
		elif not file_extension:
			error = file_name + file_extension + ' is either a directory or not a valid file'
			raise AssertionError(error)
		else:
			error = 'File extension ' + file_extension + ' not valid'
			raise AssertionError(error)

	# Opens the File, sets headers and sends POST request to IBM Watson, returns JSON response 
	def request(self,audio_format):
		url = "https://api.au-syd.speech-to-text.watson.cloud.ibm.com/instances/8d79c68b-01d0-4fbd-8ef7-c63817d41397/v1/recognize?speaker_labels=true"
		auth = ('apikey', '8ecjDiukKvweVEqbJfGflJ1bQH66eYIQelXxeHoZLIk5')

		m4a = 'm4a'
		headers_key = 'Content-Type'

		if audio_format is m4a:	
			# TODO: Convert m4a to wav
			pass
		else:
			headers_value = 'audio/' + audio_format
		
		headers = {headers_key : headers_value}
		data = open(self.file_name, 'rb').read()

		try:
		    response = requests.post(url=url,headers=headers,data=data,auth=auth)
		    response.raise_for_status()
		    jsonResponse = response.json()
		    return jsonResponse

		except HTTPError as http_err:
		    print(f'HTTP error occurred: {http_err}')
		except Exception as err:
		    print(f'Other error occurred: {err}')

	# Prints the desired Output -- format "Person Number - time-time" --example "Person 1 - 1:00-1:52" 
	def printResponse(self, response):
		response_speakers = response['speaker_labels']
		speakers = set()
		for i in range(len(response_speakers)):

			if (response_speakers[i]['speaker'] + 1) not in speakers:
				if i == 0:
					speakers.add(response_speakers[i]['speaker'] + 1)
					print('Person ' + str(response_speakers[i]['speaker'] + 1) + ' - ' + str("%.2f" % response_speakers[i]['from']).replace('.',':') + '-', end = "")
				else:
					speakers.add(response_speakers[i]['speaker'] + 1)
					print(str(response_speakers[i-1]['to']).replace('.',':'))
					print('Person ' + str(response_speakers[i]['speaker'] + 1) + ' - ' + str("%.2f" % response_speakers[i]['from']).replace('.',':') + '-', end = "")
			
			elif response_speakers[i]['final'] == True:
					print("%.2f" % str(response_speakers[i-1]['to']).replace('.',':'))

if __name__ == "__main__":
	file_name = sys.argv[1]


	obj = Transcribe(file_name)
	
	audio_format = obj.identifyFormat()
	# print(audio_format)

	response = obj.request(audio_format)
	# print(response)

	obj.printResponse(response)



	