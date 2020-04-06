# InstagramAutoBot
Bot for Automating Multiple Instagram accounts
It downloads images from Reddit and posts them on to Instagram, replies to and likes "Good" comments
# Requirements
- Python 3.5 (or higher)
- The [Instabot](https://github.com/instagrambot/instabot) library (pip install -U instabot)
- The [PRAW](https://praw.readthedocs.io/en/latest/getting_started/installation.html) library (pip install praw)
- The [Pillow](https://pillow.readthedocs.io/en/stable/) library (pip install pillow)
# Setup
1. Clone the repository and ensure you have all the requirements
2. Create a [Reddit App](https://www.reddit.com/prefs/apps)
3. Enter the client id and client secret of your Reddit App into app.py (lines 15-16)
4. Create a folder in "/accounts/" and name it the name of your instagram account.
5. Copy the files from "/accounts/account name/" into the folder you just created and enter the details for that account into data.json
6. Repeat steps 4 + 5 until you have added all the accounts you wish to add, then delete "/accounts/account name/"
7. Run app.py
