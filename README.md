# What is this app?
This application is a simple command-line interface that provides data processing for various formats such as JSON, XML, CSV, and offers functionality tailored for both users and administrators.

# Key Features
- Reads and integrates data from different formats (JSON, XML, CSV) located in the specified directory.
- Provides commands for users and administrators to manipulate data based on their respective needs.
- User actions enable the display and retrieval of information related to a user.
- Administrator actions offer functionalities tailored for administrators, such as displaying all accounts and presenting information about the oldest account.

### Import and integrate data ###
- Validate emails - validation criteria is listed below, reject entries without a valid email address
- Reject entries without provided telephone number
- Remove duplicates(by telephone number or email) from the merged dataset. Save the newer entry based on the timestamp.
- Store telephone numbers as 9 digits, remove any special characters and leading zeros (+48123456789, 00123456789, (48) 123456789, 123 456 789, all of these should be stored as 123456789)
- All telephone numbers has been generated in a way that after removing special chars and leading zeros, there will always be a valid 9-digit number. For the purposes of this exercise you can omit further validation.

### Validation Criteria for Emails: ###
- Email must contain only one "@" symbol.
- The part before "@" must be at least 1 character long.
- The part between "@" and "." must be at least 1 character long.
- The part after the last "." must be between 1 and 4 characters long, containing only letters and/or digits.

# ENV #
IDE: Atom <br>
OS: MacOS <b>
Python: 3.11.0 <br>
Libraries: pandas, argparse etc (requirements.txt) <br>

# DEMO #

## Example of integrated data
|firstname | telephone_number	| email	| password	| role | created_at	| children |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Kathryn	| 108835339	| carterlindsey@example.org	| +sUVpIkkY6	| user	| 2023-11-20 07:22:51	| [] |
| Michael	| 667574950	| kimberlymartin@example.org	| ns6REVen+g |	admin	| 2023-11-19 20:42:33 |	[{'name': 'Justin', 'age': 15}, {'name': 'Sarah', 'age': 10}] |
| Joseph	| 756037486	| lisa93@example.com	| !q62J8^sYb	| user	| 2023-11-13 14:10:09	| [] |
| Dawn	| 717279856	| briancollins@example.net	| R9AjA5nb$!	| admin	| 2023-11-13 01:28:53	| [] |
| Steven	| 691250247	| weisskristina@example.net	| 9T1zNeAN(2	| user	| 2023-11-10 09:52:49	| [] |
| George	| 681988567	| michelle93@example.org	| +hL*hdte2H	| admin	| 2023-11-08 16:38:28	| [{'name': 'Samantha', 'age': 6}] |
| Donna	| 504140673	| ngutierrez@example.net | @9TcRo15As	| user	| 2023-11-06 02:10:33	| [{'name': 'Jackie', 'age': 9}, {'name': 'Mitchell', 'age': 6}] |
<br>
Command format
```
python script.py <command> --login <login> --password <password>
```

## Admin Action ##
### Print The Number of All Valid Accounts ###
```
python script.py print-all-accounts --login ashleyhall@example.net --password '#0R0UT&yw2'

84
```
Meanwhile user can not access this command.
```
python script.py print-all-accounts --login 108835339 --password '+sUVpIkkY6'

User has no permission for this command!
```
#### Print The Longest Existing Account ###
```
python script.py print-oldest-account --login ashleyhall@example.net --password '#0R0UT&yw2'

name: Justin
email_address: opoole@example.org
created_at: 2022-11-25 02:19:37
```
Meanwhile user can not access this command.
```
python script.py print-oldest-account --login 108835339 --password '+sUVpIkkY6'

User has no permission for this command!
```
### Group Children by Age ###
```
python script.py group-by-age --login ashleyhall@example.net --password '#0R0UT&yw2'

age: 13, count: 2
age: 15, count: 2
age: 18, count: 2
age: 3, count: 3
age: 5, count: 3
age: 10, count: 3
age: 14, count: 3
age: 4, count: 4
age: 6, count: 4
age: 7, count: 4
age: 9, count: 4
age: 12, count: 4
age: 1, count: 5
age: 2, count: 5
age: 16, count: 5
age: 8, count: 6
age: 11, count: 6
age: 17, count: 9
```
Meanwhile user can not access this command.
```
python script.py group-by-age --login 108835339 --password '+sUVpIkkY6'

User has no permission for this command!
```
## User Action ##
### Print Children ###
1. User & No Children
```
$ python script.py print-children --login 108835339 --password '+sUVpIkkY6'

No children found for this user.
```
2. User & Having children
```
python script.py print-children --login matthewdecker2@example.com --password '2p$v9zPt1+'

Jonathan, 1
Natalie, 11
```
3. Admin has access too.
```
python script.py print-children --login 232756993 --password '@%xHuZl)9l'

Danielle, 11
Dustin, 7
Karen, 7
```
### Find Users with Children of Same Age ###
1. User & No Children
```
Profil-assignment % python script.py find-similar-children-by-age --login woodsjerry@example.com --password 'z2Y%0Hbcsi'

No children found for this user.
```
2. User & Having Children
```
python script.py find-similar-children-by-age --login 401629185 --password 'WAq7M2xG&K'

Amanda, 208579481: George, 8
Amy, 361568741: Sara, 8
Chad, 882294581: April, 8
Christopher, 743328816: Zachary, 8; James, 9
Curtis, 107058738: Eric, 8
Donna, 504140673: Jackie, 9
Sandra, 267687714: Robert, 9
```
3. Admin has access too.
```
python script.py find-similar-children-by-age --login ashleyhall@example.net --password '#0R0UT&yw2'

Brian, 174746366: Victoria, 1
Don, 612660796: Judith, 1
Eric, 110355347: Mary, 1
Kevin, 227397825: Kristin, 14
Madeline, 441935720: Jonathan, 1
Michael, 736121560: Angela, 14
```

## Invalid Credential ##
```
python script.py print-all-accounts --login woodsjerry@example.com --password 'z2Y%afafadi'

Invalid Login
```

## Author ##
Seita Fujiwara 2023
