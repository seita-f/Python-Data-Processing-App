import argparse
import sys
from settings import *

class CommandManager:
    def __init__(self, datasets):
        self.datasets = datasets
        self.valid_credentials = False
        self.admin = False # 1-Admin, 0-User

    def parse_arguments(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('command', choices=COMMAND_CHOICES) # settings.py
        parser.add_argument('--login', required=True, help='User login (email or 9-digit telephone number)')
        parser.add_argument('--password', required=True, help='User password')
        args = parser.parse_args()

        self.command = args.command
        self.login = args.login
        self.password = args.password

    def check_credentials(self):
        filtered_data = self.datasets[(self.datasets['email'] == self.login) | (self.datasets['telephone_number'] == self.login)]

        if not filtered_data.empty:
            if filtered_data['password'].iloc[0] == self.password:
                # print("Valid data!")
                self.valid_credentials = True
                self.is_admin(filtered_data)
                self.user = filtered_data

    def is_admin(self, data):
        if(data['role'].iloc[0] == 'user'):
            self.admin = False
        if(data['role'].iloc[0] == 'admin'):
            self.admin = True

    def perform_command(self):
        if self.valid_credentials == False:
            print("Invalid Login")
            sys.exit()

            # Note: switch statment for the task can be here
