#!/usr/bin/env python3

import os, sys
import librosa
import requests, json
import datetime
import time
import warnings
from dotenv import load_dotenv
from requests.exceptions import HTTPError


class SpeakerDiarisation:

	def __init__(self,file_name):
		self.file_name = file_name


	# Validates the file, checks for the valid file extension and returns audio-format
	def identifyFormat(self):
		valid_extensions = ('.mp3','.ogg','.wav','.m4a','.flac', '.mpeg', '.aac')
		file_path, file_extension = os.path.splitext(self.file_name)
		if file_extension in valid_extensions:
			return file_extension[1:]
		elif not file_extension:
			error = file_name + file_extension + ' is either a directory or not a valid file'
			raise AssertionError(error)
		else:
			error = 'File extension ' + file_extension + ' not valid'
			raise AssertionError(error)


	# Converts m4a/aac file to wav, stores is as a temporary file, and replaces the object's filename with temp.wav
	def convert_file_to_wav(self):
		print("Converting file to wav format...")
		start_time = time.time()
		data, sampling_rate = librosa.load(self.file_name,sr=16000)
		librosa.output.write_wav('temp.wav', data, sampling_rate)
		self.file_name = 'temp.wav'
		end_time = time.time()
		print("Finished conversion to wav format in " + self.seconds_to_minutes(end_time - start_time) + " seconds")


	# Opens the File, sets headers, sends POST request to IBM Watson Text-to-Speech API, & returns JSON response 
	def request(self,audio_format):
		load_dotenv()

		url = os.getenv('SPEECH_TO_TEXT_URL')

		api_key = os.getenv('SPEECH_TO_TEXT_APIKEY')
		auth = ('apikey', api_key)

		headers_key = 'Content-Type'

		if audio_format == 'm4a' or audio_format == 'aac':	
			self.convert_file_to_wav()
			headers_value = 'audio/wav'
		else:
			headers_value = 'audio/' + audio_format
		
		headers = {headers_key : headers_value}
		data = open(self.file_name, 'rb').read()

		try:
			print("Sending Request to Watson Speech-to-text API...")
			start_time = time.time()
			response = requests.post(url=url,headers=headers,data=data,auth=auth)
			end_time = time.time()
			print("Time taken by API: " + self.seconds_to_minutes(end_time - start_time) + " minutes")
			response.raise_for_status()
			jsonResponse = response.json()
			# with open('temp.json','w') as f:
			# 	f.write(jsonResponse)
			return jsonResponse

		except HTTPError as http_err:
			print(f'HTTP error occurred: {http_err}')
		except Exception as err:
			print(f'Other error occurred: {err}')


	# Converts Seconds to Minutes:Seconds OR Hours:Minutes:Seconds
	def seconds_to_minutes(self,seconds):
		time = str(datetime.timedelta(seconds=round(seconds,0)))
		return time[2:] if time[0] == '0' else time


	# Prints the desired Output -- format "Person Number - time-time" --example "Person 1 - 1:00-1:52" 
	def printResponse(self, response):
		response_speakers = response['speaker_labels']
		speakers = set()
		current_speaker = 0
		for i in range(len(response_speakers)):

			if (response_speakers[i]['speaker'] + 1) not in speakers:
				speakers.add(response_speakers[i]['speaker'] + 1)
				current_speaker = response_speakers[i]['speaker'] + 1				
				if i > 0:
					print(self.seconds_to_minutes(response_speakers[i-1]['to']))
				print('Person ' + str(response_speakers[i]['speaker'] + 1) + ' - ' + 
					self.seconds_to_minutes(response_speakers[i]['from']) + '-', end = "")

			elif response_speakers[i]['final'] == True:
				print(self.seconds_to_minutes(response_speakers[i-1]['to']))
				print('Person ' + str(response_speakers[i]['speaker'] + 1) + ' - ' + 
					self.seconds_to_minutes(response_speakers[i]['from']) + '-', end = "")
				print(self.seconds_to_minutes(response_speakers[i]['to']))

			else:
				if current_speaker != response_speakers[i]['speaker'] + 1: 
					current_speaker = response_speakers[i]['speaker'] + 1
					print(self.seconds_to_minutes(response_speakers[i-1]['to']))
					print('Person ' + str(response_speakers[i]['speaker'] + 1) + ' - ' + 
						self.seconds_to_minutes(response_speakers[i]['from']) + '-', end = "")

		if (self.file_name) == 'temp.wav':
			os.remove('temp.wav')


if __name__ == "__main__":
	file_name = sys.argv[1]

	# For ignoring UserWarnings
	warnings.filterwarnings("ignore")

	speakerDiarisation = SpeakerDiarisation(file_name)
	
	audio_format = speakerDiarisation.identifyFormat()
	# print(audio_format)

	response = speakerDiarisation.request(audio_format)
	# print(response)

	# with open("response.json", "r") as read_file:
	# 	response = json.load(read_file)
	
	speakerDiarisation.printResponse(response)



	