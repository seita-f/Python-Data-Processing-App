import os
import pandas as pd
# from email_validator import validate_email, EmailNotValidError
import re
import json
import xml.etree.ElementTree as ET  # Add this line to import ElementTree

# regrex
regrex_csv_children = r'([A-Za-z]+)\s*\((\d+)\)'
regex_email = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z0-9]{1,4}\b'


class DataProcessor:

    def __init__(self, data_directory):
        self.data_directory = data_directory
        self.json_data = pd.DataFrame()  # DataFrame obj
        self.xml_data = pd.DataFrame()
        self.csv_data = pd.DataFrame()

    def walk_tree(self):
        """ Walk data_directory trees, fetch the files and merge. """
        for curDir, dirs, files in os.walk(self.data_directory):
            for file in files:
                file_path = os.path.join(curDir, file)
                if file.endswith(".json"):
                    self.json_data = pd.concat([self.json_data, pd.read_json(file_path)])
                if file.endswith(".xml"):
                    self.xml_data = pd.concat([self.xml_data, pd.read_xml(file_path)])
                if file.endswith(".csv"):
                    self.csv_data = pd.concat([self.csv_data, pd.read_csv(file_path, delimiter=';')])

        # Apply child parsing functions to each row
        self.csv_data['children'] = self.csv_data['children'].fillna('').apply(self.parse_csv_children)
        self.xml_data['children'] = self.xml_data['children'].fillna('').apply(self.parse_xml_children)

    def parse_csv_children(self, children_str):
        matches = re.findall(regrex_csv_children, children_str)
        children_list = [{'name': name, 'age': int(age)} for name, age in matches]
        return children_list

    def parse_xml_children(self, children_element):
        # Check if there are elements before parsing
        if children_element is None or not list(children_element):
            return []

        # Parse the XML children element and convert it to a list of dictionaries
        children_list = [{'name': child.find('name').text, 'age': int(child.find('age').text)} for child in children_element.findall('child')]
        return children_list

    def is_valid_email(self, email):
        """ check if an email is valid format """
        if (re.fullmatch(regex_email, email)):
            return True
        else:
            # DEBUG
            # print(f'{email} is invalid format')
            return False

    def store_phone_number_nine_digits(self, telephone_number):
        """ remove special characters and leading zeros and store as 9 digits"""
        # remove specific characters
        telephone_number = telephone_number.replace('+', '').replace('(', '').replace(')', '').replace(' ', '')

        # remove country code
        try:
            if len(telephone_number) == 9: # perfect case
                return telephone_number
            elif len(telephone_number) == 11: # with country code
                return telephone_number[2:]
            else:
                raise ValueError("Invalid telephone number length")
        except ValueError as e:
            print(f"Error!!: {e}")

    def import_data(self):
        """ Importing data, check the validation and merge """

        self.walk_tree()
        # Merge datasets
        merged_data = pd.concat([self.json_data, self.xml_data, self.csv_data])

        # Get only valid email
        merged_data = merged_data[merged_data['email'].apply(self.is_valid_email)]

        # Reject entries without a valid telephone number
        merged_data = merged_data[merged_data['telephone_number'].notnull()]

        # Store telephone numbers as 9 digits, remove special characters, leading zeros
        # and country code
        merged_data['telephone_number'] = merged_data['telephone_number'].apply(self.store_phone_number_nine_digits)

        # DEBUG
        # Display duplicates based on email
        # self.display_duplicates(merged_data, 'email')
        # Display duplicates based on telephone_number
        # self.display_duplicates(merged_data, 'telephone_number')

        # Remove duplicated row and store the data with newer timestamp
        merged_data['created_at'] = pd.to_datetime(merged_data['created_at']) # Sort the DataFrame by date in descending order
        merged_data = merged_data.sort_values('created_at', ascending=False)

        # Remove duplicated rows and keep newest one
        merged_data = merged_data.drop_duplicates(subset=['telephone_number'], keep='first')
        merged_data = merged_data.drop_duplicates(subset=['email'], keep='first')

        # Fix index
        merged_data = merged_data.reset_index(drop=True)

        return merged_data;

    def __str__(self):
        return self.data_directory
