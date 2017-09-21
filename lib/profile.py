
import datetime
import time
import xml.etree.ElementTree
import urllib.parse
import html

import requests

from .chatango.constants import FONT_FACES

class Profile(object): # TO-DO: Change this to be usable by the user to get Chatango profiles other than the bots
    def __init__(self, user):
        self.user = user
        self.user_auth = self.user.get_auth_token()
        self.age = None
        self.gender = None
        self.location = None
        self.show_in_user_directory = False
        self.mini_bio = None
        self.get_profile()

    def set_age(self, age):
        if isinstance(age, int) or age.isdigit():
            age = int(age)
            if 13 <= age <= 149:
                self.age = age

    def set_gender(self, gender):
        gender = gender.upper()
        if gender in ["F", "M"]:
            self.gender = gender

    def set_location(self, location):
        if location.isdigit() or location.isalpha():
            if location.isalpha():
                location = location.capitalize()
            self.location = location

    def set_mini(self, mini):
        self.mini_bio = html.escape(mini)

    def set_show_in_user_directory(self, boolean):
        self.show_in_user_directory = boolean

    def get_profile(self):
        try:
            if len(self.user_auth[1]) >= 2:
                second_letter = self.user.name.lower()[1]
            else:
                second_letter = self.user.name.lower()[0]
            url = "http://ust.chatango.com/profileimg/" + self.user.name.lower()[0] + "/" + second_letter + "/" + self.user.name.lower() + "/mod1.xml"
            request = requests.get(url)
            xmldata = xml.etree.ElementTree.fromstring(request.text)
            for child in xmldata:
                if child.tag == "body":
                    self.mini_bio = urllib.parse.unquote(child.text)
                elif child.tag == "s":
                    self.gender = child.text
                elif child.tag == "b":
                    timestamp = time.mktime(
                        datetime.datetime.strptime(child.text, "%Y-%m-%d").timetuple()
                    )
                    difference = int(time.time() - timestamp)
                    years = int(difference / 31557600)
                    self.age = years
                elif child.tag == "l":
                    self.location = child.text
        except:
            pass

    def update(self):
        url = "http://chatango.com/updateprofile"
        def bool_to_checked(boolean):
            if boolean:
                return "checked"
            else:
                return "unchecked"
            return "checked"
        data = {
            "s": self.user_auth,
            "auth": "token",
            "arch": "h5",
            "src": "group",
            "action": "update",
            "age": str(self.age),
            "gender": self.gender,
            "location": self.location,
            "line": self.mini_bio,
            "dir": bool_to_checked(self.show_in_user_directory)
        }
        requests.post(
            url, data=data, headers={
                "Origin": "http://st.chatango.com",
                "User-Agent": "Mozilla 5/0"
            }
        )
        self.get_profile()

class Style(object): # Jesus christ
    def __init__(self):
        self.name_color = "000"
        self.font_color = "000"
        self.font_face = "0"
        self.font_size = "11"

    def set_font_face(self, name):
        font_face_index = FONT_FACES.get(name, None)
        if not isinstance(font_face_index, type(None)):
            self.font_face = font_face_index

    def set_font_size(self, size):
        if isinstance(size, (str, int)):
            if isinstance(size, str) and size.isdigit():
                size = int(size)
            if 9 <= size <= 22:
                if size < 10:
                    size = "09"
                self.font_size = size

    def set_font_color(self, color):
        # TO-DO: verify hex
        self.font_color = color

    def set_name_color(self, color):
        self.name_color = color
