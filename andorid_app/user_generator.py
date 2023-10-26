
import requests,time,random
from geopy import distance
import threading

SERWER_ADRESS = "http://afternoon-headland-3098991.herokuapp.com/"
# SERWER_ADRESS = "http://127.0.0.1:8000/"
TOKEN = ""
home_LAT = "53.450"
home_LON = "14.517"

work_LAT = "53.421"
work_LON = "14.517"


for x in range(47730,500000):
    for adress in ["http://127.0.0.1:8000/","http://afternoon-headland-3098991.herokuapp.com/"]:
        SERWER_ADRESS = adress
        if SERWER_ADRESS == "http://127.0.0.1:8000/" and x < 21000:
            continue
        try:
        #         # Create new user
            start = time.time()
            new_user = requests.post(SERWER_ADRESS+"api_new_user/",{"username":f"TestUser{x}","password":"1","first_name":"a","second_name":"b","age":18,"email":"","phone":""})
            # print(new_user.json())

            token = requests.post(SERWER_ADRESS+"api_login/",{"username":f"TestUser{x}","password":"1"})
            # print(token.json()['token'])
            # time.sleep(0.02)

            headers = {"Authorization":f"Token {token.json()['token']}"}
        #
            z = requests.post(SERWER_ADRESS+"api_geoloc/",headers=headers,data={"action":"update_user_pos","lat":f"53.{random.randint(39300,47600)}","lon":f"14.{random.randint(49700,58000)}","distance":"200","home_lat":home_LAT,"home_lon":home_LON,"work_lat":work_LAT,"work_lon":work_LON,"friendsOnly":False})
            # print(x.text)
            # prepare = requests.post(SERWER_ADRESS+"api_geoloc/",headers=headers,data={"action":"prepare_friends_lists"})
            end = time.time()
            print(z.status_code)
            print(x)
            print("czas : ", end-start)
        except:
            print("nie udało się stworzyć usera: ", x)





# Czas tworzenia usera przy 27k w bazie:  5.6324615478515625
# Może tworzyć ich w kilku wątkach ?