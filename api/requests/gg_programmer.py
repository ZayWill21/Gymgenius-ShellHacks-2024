import json
from ics import Calendar, Event
from datetime import datetime, timedelta
from .gg_request import gg_Request
from .gg_datatype import gg_Datatype
import re

class Programmer(gg_Request):
    def __init__(self, prompt, datatype, api):
        super().__init__(prompt, datatype, api)
        self.file = None

    def make_request(self, conversation_history, user_id):
        req_string = "Use the following prompt to create a workout routine\n" + \
                     "The prompt is: " + "\"" + self.prompt + "\"" + "\n" + \
                     "Then answer that input as a " + gg_Datatype.to_string(self.datatype) + ".\n" + \
                     "Base the program you create highly off of the prompt but also take influence from the conversation history" + conversation_history + \
                     "Note the date and time is " + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "Your response must be an ICS file make it so monday-sunday from 5 to whatever time necessary, has all data based on the program generated. Also make sure the time and date are relative to the provided current onees. here is an example of a program in JSON but you MUST MUST MUST MUST provide your response in terms of an ICS file: " + gg_Datatype.get_preset(self.datatype)
        self.last_response = self.api.send_request(self.datatype, req_string)
        # Extract the raw content from the response
        raw_content = self.last_response

        # Use regex to extract valid ICS data
        ics_content = re.search(r'(BEGIN:VCALENDAR.*END:VCALENDAR)', raw_content, re.DOTALL)

        if ics_content:
            # Create and save the ICS file
            with open("schedules/"+str(user_id) + '_schedule.ics', 'w') as file:
                file.write(ics_content.group(0))  # Write only the matched ICS content
                self.file = file
            print("ICS file created: schedule.ics")
        return self.last_response

        
