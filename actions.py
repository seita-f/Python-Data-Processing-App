import pandas as pd
from collections import Counter

class UserAction():
    """ Define User Action """

    def __init__(self, datasets, user):
            self.datasets = datasets
            self.user = user
            self.user_actions = {
                'print_children': self.print_children,
                'find_similar_children_by_age': self.find_similar_children_by_age,
            }

    def print_children(self):
        """ Display information about the user's children. Sort children alphabetically by name """

        # When user has childeren
        if len(self.user['children'].iloc[0]) > 0:

            children_list = self.user['children'].iloc[0]
            sorted_children = sorted(children_list, key=lambda x: x.get('name'))

            # print childrens
            for child in sorted_children:
                print(f"{child.get('name')}, {child.get('age')}")
        else:
            print(f"No children found for this user.")


    def find_similar_children_by_age(self):
        """Find users with children of the same age as at least one own child,
        print the user and all of his children data. Sort children alphabetically by name.
        """
        matched_data = {'Parent': [], 'Parent Telephone': [], 'Child': [], 'Child Age': []}

        if len(self.user['children'].iloc[0]) > 0:

            user_name = self.user['firstname'].iloc[0]
            user_tel_number = self.user['telephone_number'].iloc[0]
            user_children = self.user['children'].iloc[0]

            # Iterate over user children
            for user_child in user_children:

                user_child_age = user_child.get('age')

                # Iterate over users in the dataset
                for index, row in self.datasets.iterrows():
                    if row['telephone_number'] != user_tel_number:
                        parent_name = row['firstname']
                        parent_telephone = row['telephone_number']

                        # Iterate over children for a user in the dataset
                        for dataset_child in row['children']:
                            if dataset_child['age'] == user_child_age:
                                matched_data['Parent'].append(parent_name)
                                matched_data['Parent Telephone'].append(parent_telephone)
                                matched_data['Child'].append(dataset_child.get('name'))
                                matched_data['Child Age'].append(dataset_child.get('age'))
        else:
            print('No children found for this user.')
            return

        if not matched_data['Parent']:
            print('There are no children of the same age')
        else:
            # Convert the matched data dictionary to a DataFrame
            result_df = pd.DataFrame(matched_data)

            # Group the DataFrame by parent, filter unique child names, and format the output
            grouped_result = result_df.groupby(['Parent', 'Parent Telephone']).apply(
                lambda x: '; '.join(f"{name}, {age}" for name, age in set(zip(x['Child'], x['Child Age'])))
            )

            # Print the grouped results
            for (parent, telephone), children_info in grouped_result.items():
                print(f"{parent}, {telephone}: {children_info}")


class AdminAction(UserAction):
    """ Define Admin Action """

    def __init__(self, datasets, user):
        super().__init__(datasets, user)  # Call the constructor of the base class (UserAction)
        self.user_actions = {
            'print_all_accounts': self.print_all_accounts,
            'print_oldest_account': self.print_oldest_account,
            'group_by_age': self.group_by_age,
        }

    def import_data_exel(self):
        """ Import data in excel """
        self.datasets.to_excel('data.xlsx', index=False)
        print("Data is imported in exel file")

    def print_all_accounts(self):
        """ Print the total number of valid accounts """
        print(len(self.datasets))

    def print_oldest_account(self):
        """ Print information about the account with the longest existence """
        oldest_accont = self.datasets.iloc[-1]  # suppose datasets is alreay sorted
        print(f'name: {oldest_accont["firstname"]}')
        print(f'email_address: {oldest_accont["email"]}')
        print(f'created_at: {oldest_accont["created_at"]}')

    def group_by_age(self):
        """ Group accounts by age and print the count for each age """
        age_counts = self.datasets['children'].apply(lambda x: [child['age'] for child in x] if isinstance(x, list) else []).explode().value_counts()

        # Count -ascending, then Age -ascending.
        count_sorted_ages = sorted(age_counts.items(), key=lambda x: (x[1], x[0]))

        for age, count in count_sorted_ages:
            print(f'age: {age}, count: {count}')
