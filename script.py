""" Main File """
import argparse  # Argument handling
from settings import *
import pandas as pd

# from dataProcessor import DataProcessor
from dataProcessor import DataProcessor
from command import CommandManager
from actions import UserAction, AdminAction


USER = "user"
ADMIN = "admin"

def no_permission_msg():
    print("User has no permission for this command!")


""" Importing Data """
dataProcessor = DataProcessor(DATA_DIR)
datasets = dataProcessor.import_data()


if __name__ == "__main__":

    """ Argument Handling """
    commandManager = CommandManager(datasets)
    commandManager.parse_arguments()  # get & read args
    commandManager.check_credentials() # check if login and password are matching
    commandManager.perform_command() # If not, dispaly error
    user_data = commandManager.user
    # print(user_data) # DEBUG

    # user type
    user_type = user_data['role'].iloc[0] # user or admin


    """ Task Handling """
    userAction = UserAction(datasets, user_data)
    adminAction = AdminAction(datasets, user_data)

    match commandManager.command:
        case "import-data":
            if(user_type == USER):
                no_permission_msg()
            if(user_type == ADMIN):
                adminAction.import_data_exel()
            pass

        case "print-all-accounts":
            if(user_type == USER):
                no_permission_msg()
            if(user_type == ADMIN):
                adminAction.print_all_accounts()
            pass

        case "print-oldest-account":
            if(user_type == USER):
                no_permission_msg()
            if(user_type == ADMIN):
                adminAction.print_oldest_account()
            pass

        case "group-by-age":
            if(user_type == USER):
                no_permission_msg()
            if(user_type == ADMIN):
                adminAction.group_by_age()
            pass

        case "print-children":
            if(user_type == USER):
                userAction.print_children()
            if(user_type == ADMIN):
                adminAction.print_children()
            pass

        case "find-similar-children-by-age":
            if(user_type == USER):
                userAction.find_similar_children_by_age()
            if(user_type == ADMIN):
                adminAction.find_similar_children_by_age()
            pass

        case _:
            print("ERROR")
