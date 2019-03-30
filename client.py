import os
import platform
import requests
import time
import sys

HOST = "localhost"
PORT = "1104"
CMD=token=''

def __api__():
    return 'http://' + HOST + ":" + PORT + "/" + CMD

def printres(res):
    a=res["tickets"].split('-')
    z=0
    while z<int(a[1]):
        h=res['block {}'.format(z)]
        print('subject :'+h['subject'])
        print('id :'+str(h['id']))
        print('status :'+h['status'])
        print('body :'+h['ask'])
        if h['answer']:
            print('answer :'+h['answer'])
        else:
            print('answer :' + "")
        print('date created :' + h['date'])
        print("<================================>")
        z=z+1

def clear():
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')

def show_func():
    # print("USERNAME : "+USERNAME+"\n"+"API : " + API)
    print("""What Do You Prefer To Do :
    1. Send Ticket
    2. Get Ticket Cli
    3. Close Ticket
    4. Get Ticket Mod
    5. Response to Ticket
    6. Change Status
    7. Change Access
    8. Logout
    9. Exit
    """)

while True:
    clear()
    print("""WELCOME TO TICKET CLIENT
    Please Choose What You Want To Do :
    1. signin
    2. signup
    3. exit
    """)
    status = input()
    if status == '1':
        clear()
        while True:
            print("username : \n")
            username = input()
            print("password : \n")
            password = input()
            CMD = "login"
            r=requests.post(__api__(),data={'username':username,'password':password}).json()

            if r['code'] == '200':
                clear()
                print("Username an Password IS CORRECT\nLogging You in ...")
                token = r['token']

                time.sleep(2)
            else:
                clear()
                print("Username an Password IS INCORRECT\nTRY AGAIN ...")
                time.sleep(2)
                break
            while True:
                clear()
                show_func()
                func_type = input()
                if func_type == '1':
                    clear()
                    CMD = "sendticket"
                    subj=input("what is your subject: ")
                    txt= input("what is your txt: ")
                    data = requests.post(__api__(),data={'token':token,'text':txt,'subject':subj}).json()
                    print(data['message'] + '\n')
                    input("Press Any Key To Continue ...")
                if func_type == '2':
                    clear()
                    CMD = "getticketcli"
                    status=input("what kind of status do you need?? open,closed,waiting: ")
                    data = requests.get(__api__(),params={'token':token,'status':status}).json()
                    if data['code']=='200':
                        printres(data)
                    else:
                        print(data["message"]+'\n')
                    input("Press Any Key To Continue ...")
                if func_type == '3':
                    clear()
                    idn=input("ticket id : ")
                    CMD = "closeticket"
                    data = requests.post(__api__(),data={'token':token,'commentId':idn}).json()

                    print(data['message']+'\n')
                    input("Press Any Key To Continue ...")
                if func_type == '4':
                    clear()
                    CMD = "getticketmod"
                    status = input("what kind of status do you need?? open,closed,waiting: ")
                    data = requests.get(__api__(), params={'token': token, 'status': status}).json()

                    if data['code'] == '200':
                        printres(data)
                    else:
                        print(data["message"] + '\n')
                    input("Press Any Key To Continue ...")
                if func_type == '5':
                    clear()
                    CMD = "restoticketmod"
                    ans = input("what is your answer? ")
                    idn = input("ticket id :")
                    data = requests.post(__api__(),data={'token':token,'commentId':idn,'text':ans}).json()

                    print(data['message']+'\n')
                    input("Press Any Key To Continue ...")
                if func_type == '6':
                    clear()
                    CMD = "changestatus"
                    status = input("choose status? open,closed,waiting :")
                    idn = input("ticket id :")
                    data = requests.post(__api__(),
                                                  data={'token': token, 'commentId': idn, 'status': status}).json()

                    print(data['message']+'\n')
                    input("Press Any Key To Continue ...")
                if func_type == '7':
                    clear()
                    CMD = "changeaccess"
                    username = input("what username do you need to change access :")
                    rootpass = input("what is root password? ")
                    admin = input("0 for normal & 1 for admin :")
                    data = requests.post(__api__(),
                                                  data={'username': username, 'rootPass': rootpass, 'admin': admin}).json()

                    print(data['message']+'\n')
                    input("Press Any Key To Continue ...")
                if func_type == '8':
                    clear()
                    CMD = "logout"
                    data = requests.post(__api__(),data={'token': token}).json()


                    print(data['message']+'\n')
                    input("Press Any Key To Continue ...")
                if func_type== '9':
                    sys.exit()





    elif status == '2':
        clear()
        while True:
            print("To Create New Account Enter The Authentication\n")
            username= input("USERNAME : ")

            password= input("PASSWORD : ")
            CMD = "signup"
            clear()
            data = requests.post(__api__(),
                                          data={'username': username, 'password': password}).json()

            if str(data['code']) == "200":
                print("Your Acount Is Created\n"+"Your Username :"+username+"\n")
                input("Press Any Key To Continue ...")
                break
            else :
                print(data['code']+"\n"+"Try Again")
                input("Press Any Key To Continue ...")
                clear()

    elif status == '3':
        sys.exit()
    else:
        print("Wrong Choose Try Again\n")
