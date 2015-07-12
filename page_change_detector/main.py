import re
import mechanize
import os.path
import random
import easygui
import time

#username = 'kink1134'
username = 'appliedmath'
filename = 'imgur_'+username+'.txt'

#username = 'appliedmath'
br = mechanize.Browser()
response = br.open("http://imgur.com/user/"+username)
    

# check if user data exists
# if the user data exists, retreive first comment, compare to saved comment

user_dat_exists = os.path.isfile(filename)

## retreive first comment
stringform = response.read()
r1 = stringform.split('<span>')
r2 = []
#print r1[0]
#print r1[0].split('</span>')[0]

#for string in r1:
#    r2.append(string.split('</span>')[0])
first_comm = r1[1].split('</span>')[0]
first_comm = first_comm.strip()


#print len(first_comm)
#print first_comm
#for string in r2:
#    print string
#print r2

if user_dat_exists:
    f = open(filename,'r')
    data = str(f.read()).strip()
    #print 'data:',data,'   first_comm:',first_comm
    f.close()

    if data != first_comm:
        easygui.msgbox("New comment detectd! user:"+username, title="simple gui")
        print 'saving new first comment'
        f = open(filename,'w')
        f.write(first_comm)
        f.close()

    else:
        #sleeptime = 60*random.random()
        print 'no changes yet...'
    
# if user does not exist, retreive and save first comment        
if not(user_dat_exists):
    f = open(filename,'w')
    f.write(first_comm)
    f.close()

time.sleep(60*30+random.random())
