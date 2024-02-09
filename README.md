# Convocation System
## Setup Guide
Before you can run the program, you need to first make sure you have a Google account to use for sending emails.
### Google Account
1. Create a new Google Account (if you have an existing one, then that works too)
2. Make sure you've set up 2FA in your Google Account
3. Go to the [Google App Password](https://myaccount.google.com/apppasswords) page and fill in the necessary info.
4. You should be given your app password. Make sure you keep it and don't share it to anyone else.

### Code
1. In project/__main__.py, there should be 2 commented lines of code:
```
# app.config['MAIL_USERNAME'] = <insert google account>
# app.config['MAIL_PASSWORD'] = <insert google app password>
```
2. Un-comment the two lines and fill in the necessary info in the two fields.

## Running the code
1. In the command line, make sure to activate the virtualenv with the following command:
   
```
venv/Scripts/activate
```
   You may need to run the following command if you are getting an error saying running scripts is disabled:  
```
set-executionpolicy unrestricted
```
2. Once that is done, you can now open the program using:
```
py project/
```

## Database
When you first run the program, a database would be created inside project/instance. The database uses SQLite because PostgreSQL is far too complicated for me. If you want to add any new data/modify the data inside the newly created database, you can install a program called [DB Browser for SQLite](https://sqlitebrowser.org/) to add/edit data. Just make sure you don't edit the tables unless you know what you are doing.
