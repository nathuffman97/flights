from twilio.rest import TwilioRestClient
import os
import json


class Text:
    def __init__(self, data_path):
        file_location = os.path.join(data_path, 'twilio_data.json')
        with json.load(open(file_location, 'r')) as data_file:
            self.twilio_client = TwilioRestClient(data_file['SID'], data_file['auth'])
            self.sending_number = data_file['twilioNumber']
            self.my_number = data_file['myNumber']

    def text_me(self, message):
        self.twilio_client.message.create(body=message, from_=self.sending_number, to=self.my_number)
