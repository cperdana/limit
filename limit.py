# 
# ref  https://askubuntu.com/questions/68918/how-do-i-restrict-my-kids-computing-time
# 




#!/usr/bin/python3
import subprocess
import os
import sys
import time
import argparse



def read(f):
    try:
        return int(open(f).read().strip())
    except FileNotFoundError:
        pass

def message(disp, user):
    return "DISPLAY="+disp+" su - "+user+" -c "+'"'+\
      "notify-send 'User "+user+\
      " will be logged off in 60 seconds'"+'"'


def get_argument():
    parser = argparse.ArgumentParser()

    # parser.add_argument("user", help="user to be monitor")
    # parser.add_argument("minutes", help="maximum minutes per day", type=int)
    parser.add_argument("-c", "--config-file", help="config-file")

    parser.add_argument("-b", "--balance", help="show balance", action='store_true')

    args = parser.parse_args()
    return args

def read_config():
    with open('limit.dat') as f:
        lines = [line.rstrip() for line in f]

    users = []
    datas = {}
    for line in lines:
        if line[0:1] != "#":
            dat = line.split(";")
            datas[dat[0]] =  dat[1] 
            # users.append(data)


    return datas


def process_restricted_users(user, minutes, uselog, data):
    print(user, minutes)
    disp = data[0]
    pid = data[1]
    
    n = read(uselog)
    n = n + 1 if n != None else 0
    
    open(uselog, "wt").write(str(n))
    # when time exceeds the permitted amount, kill the process
    if int(n) + 6 > minutes*6:
        # disp = [d for d in [d[1] for d in pid] if all([":" in d, not "." in d])][0]
        
        # pids = [p[-2] for p in pid]
        # for p in pids:
        print("killing process: ", pid)
        subprocess.Popen(["kill", pid])


    elif int(n)  > minutes*6:
        msg = message(disp, user)
        print (msg)
        subprocess.Popen(["/bin/bash", "-c", msg])
        # time.sleep(60)
    else:
    	print("masa: ", n, (int(n) /6 ))

def getLoginUsers(controlled_users):
    who = subprocess.check_output(["who", "-u"]).decode("utf-8")
    desktop_logins = [l.split() for l in who.splitlines() if all([ not "pts/" in l ])]

    # users_only = [user[0] for user in users]
    users_only = controlled_users.keys()

    restricted_user = {}
    for login in desktop_logins:
        # pass
        # print(login)
        if login[0] in users_only:
            data = [login[1], login[-2]]
            print("ada ", login[0], "   data:", data)

            restricted_user[login[0]] = data
            # restricted_user.append(user)

    return restricted_user



def show_balance(users_max):
	users = users_max.keys()

	for user in users:
		# print(user, users_max[user])

		usage_file = "uselog." + user
		if os.path.exists(usage_file):
			usage = read(usage_file)
		else:
			usage = 0

		seconds_use = int(usage) * 10
		seconds_limit = int(users_max[user]) * 60

		balance = (seconds_limit - seconds_use )/60

		print("%10s  max:%3s    usage:%4s   seconds_use:%4s    seconds_limit:%7s  %10s"  % (user, users_max[user], usage, seconds_use, seconds_limit, balance ))

def main():
	USELOG = "/opt/limit/uselog."
	USELOG = "uselog."

	args = get_argument()

	users_max = read_config()

	if args.balance == True:
		# print("balance true")
		show_balance(users_max)
		exit()






	# print(users_max)

	while True:
		time.sleep(10)

		restricted_login_users = getLoginUsers(users_max)
		# print(restricted_login_users)

		datefile = "/opt/limit/currdate"
		datefile = "currdate"
		currday1 = read(datefile)

		currday2 = int(time.strftime("%d"))
		# check if the day has changed, to reset the used quantum
		if currday1 != currday2:
		    open(datefile, "wt").write(str(currday2))

		    for user in users_max.keys():
		        uselog = USELOG + user
		        try:
		            os.remove(uselog)  
		        except FileNotFoundError:
		            pass




		for user in restricted_login_users.keys():
		    max_minutes = users_max[user]
		    uselog = USELOG + user
		    process_restricted_users(user, int(max_minutes), uselog, restricted_login_users[user])



if __name__ == "__main__":
    main()
