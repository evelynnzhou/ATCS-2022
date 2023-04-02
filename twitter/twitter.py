from sqlalchemy import desc
from models import *
from database import init_db, db_session
from datetime import datetime

class Twitter:
    """
    The menu to print once a user has logged in
    """
    def print_menu(self):
        print("\nPlease select a menu option:")
        print("1. View Feed")
        print("2. View My Tweets")
        print("3. Search by Tag")
        print("4. Search by User")
        print("5. Tweet")
        print("6. Follow")
        print("7. Unfollow")
        print("0. Logout")
    
    """
    Prints the provided list of tweets.
    """
    def print_tweets(self, tweets):
        for tweet in tweets:
            print("==============================")
            print(tweet)
        print("==============================")

    """
    Should be run at the end of the program
    """
    def end(self):
        print("Thanks for visiting!")
        db_session.remove()
    
    """
    Registers a new user. The user
    is guaranteed to be logged in after this function.
    """
    def register_user(self):
        match = False
        while (match == False):
            unique = False
            while(unique == False):
                handle = input("What will your twitter handle be?\n")
                if (db_session.query(User).first() == None):
                    unique = True
                    break
                else:
                    for user in db_session.query(User).all():
                        if(handle == user.username):
                            print("That username is already taken. Try again.")
                        else:
                            unique = True
            pw = input("Enter a password: ")
            pw2 = input("Re-enter your password: ")
            if(pw == pw2):
                match = True
                break
            print("Those passwords don't match. Try again.")
        user = User(username = handle, password = pw)
        self.user = user
        db_session.add(user)
        db_session.commit()
        

    """
    Logs the user in. The user
    is guaranteed to be logged in after this function.
    """
    def login(self):
        success = False
        while(success == False):
            username = input("Username: ")
            pw = input("Password: ")
            for user in db_session.query(User).all():
                if(username == user.username):
                    if(pw == user.password):
                        print("Welcome " + user.username + "!")
                        success = True
                        self.user = user
            if(success == False):
                print("Invalid username or password")

    def logout(self):
        self.end()

    """
    Allows the user to login,  
    register, or exit.
    """
    def startup(self):
        res = input("Please select a Menu Option\n1. Login\n2. Register User\n0. Exit\n")
        if(res == "1"):
            self.login()
        elif(res == "2"):
            self.register_user()
        elif(res == "0"):
            self.end() 

    def follow(self):
        account = input("Who would you like to follow?\n")
        following = self.user.following
        alr_f = False
        for user in following:
            if(user.username == account):
                alr_f = True
        if (alr_f == True):
            print("You already follow " + user.username)
        else:
            new_follow = db_session.query(User).where(User.username == account).first()
            self.user.following.append(new_follow)
            db_session.commit()
            print("You are now following " + new_follow.username)

        

    def unfollow(self):
        account = input("Who would you like to unfollow?\n")
        following = self.user.following
        no_f = True
        for user in following:
            if(user.username == account):
                self.user.following.remove(user)
                db_session.commit()
                no_f = False
        if (no_f == True):
            print("You don't follow " + account)
        else:
            print("You no longer follow " + user.username)

    def tweet(self):
        content = input("Create Tweet: ")
        tags = input("Enter your tags separated by spaces: ")
        timestamp= datetime.now()
        tweet = Tweet(content = content, username = self.user.username, timestamp = timestamp)

        for tag in tags.split():
            new = True
            for existing_tag in db_session.query(Tag).all():
                    if(tag == existing_tag.content):
                        tweet.tags.append(existing_tag)
                        new = False
            if(new == True):
                new_tag = Tag(content = tag)
                tweet.tags.append(new_tag)
        db_session.add(tweet)
        db_session.commit()
            

    def view_my_tweets(self):
        self.print_tweets(db_session.query(Tweet).where(Tweet.username == self.user.username).all())
    
    """
    Prints the 5 most recent tweets of the 
    people the user follows
    """
    def view_feed(self):
        followed_usernames = []
        following = self.user.following
        for user in following:
            followed_usernames.append(user.username)

        self.print_tweets(db_session.query(Tweet).filter(Tweet.username.in_(followed_usernames)).order_by(desc(Tweet.timestamp)).limit(5).all())

    def search_by_user(self):
        req_user = input("Enter a username to search by: ")
        exist = False
        for user in db_session.query(User).all():
            if(user.username == req_user):
                self.print_tweets(db_session.query(Tweet).where(Tweet.username == req_user).all())
                exist = True
        if(exist == False):
            print("There is no user by that name.")

    def search_by_tag(self):
        req_tag = input("Enter a tag to search by: ")
        exist = False
        for tag in db_session.query(Tag).all():
            if(tag.content == req_tag):
                tag_obj = db_session.query(Tag).where(Tag.content == req_tag).first()
                tweets = db_session.query(Tweet).where(Tweet.tags.contains(tag_obj)).all()
                self.print_tweets(tweets)
                exist = True
        if(exist == False):
            print("There is no tweets with this tag.")

    def __init__(self):
        self.user = None

    """
    Allows the user to select from the 
    ATCS Twitter Menu
    """
    def run(self):
        init_db()

        print("Welcome to ATCS Twitter!")
        self.startup()

        
        self.print_menu()
        option = int(input(""))

        while(option != 0):
            if option == 1:
                self.view_feed()
            elif option == 2:
                self.view_my_tweets()
            elif option == 3:
                self.search_by_tag()
            elif option == 4:
                self.search_by_user()
            elif option == 5:
                self.tweet()
            elif option == 6:
                self.follow()
            elif option == 7:
                self.unfollow()
            else:
                self.logout()
            self.print_menu()
            option = int(input(""))
        
        self.end()
