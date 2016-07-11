#!/usr/bin/env python3
import os,shelve,re,requests,datetime

autof='//home//rajat//Desktop//wordpress problems' # the folder to be automated
curd=os.getcwd() #current directory
data="data" #datafile name
sol=['.py','.cpp','.c']




    
####### Create folder for new question ###################
def createf(num):  #creates a new file.
 os.chdir(autof)
 try:
  os.makedirs("question "+str(num))
  return 1
 except FileExistsError:
  return 1
##########################################################


################# updation part ___updateinfo()_____###########################
def extension(l): ##function to verify the extension of file to be py, cpp or c
 n=[]
 for i in l:
  if(sol[0] in str(i))|(sol[1] in str(i))|(sol[2] in str(i)):
   n.append(i)
 return n


def updateinfo(new=0): ## updates the info of files newly created
 os.chdir(curd)       #just for reassurance
 rec=shelve.open(data)#this opens the data file 
 dirlist=[]
 if new==0:                                     ##this condition will update evrything regardless of new or old.and delete nonexisting entries
  for folder,direct,files in os.walk(autof):
   if folder==autof:
    dirlist=direct
    continue
   rec[os.path.basename(folder)]=extension(files)
  for n in rec:
   if n not in dirlist:
      del rec[n]
 elif new==1:					##this condition will ignore old entries and will add new and will also delete non existing entries
  for folder,direct,files in os.walk(autof):
   if folder==autof:
    dirlist=direct
    continue
   if folder not in rec:
    rec[os.path.basename(folder)]=extension(files)
  for n in rec:
   if n not in dirlist:
      del rec[n]
 rec.close()
#########################################################

###################### information about teh folder #######################
def getinfo():
 os.chdir(curd)
 rec=shelve.open(data)
 for k in rec:
  if rec[k]==[]:
   print("NO sollution for "+str(k))
 rec.close()
############################################################################


#################### scrapper function to find the new question ############

def scrapper():
 web=requests.get('https://csmadeeasy.wordpress.com/category/problems-to-solve/')
 try:
  web.raise_for_status()
 except Exception as exc:
  print("the process failed")
 r=re.compile('<a href="https://csmadeeasy.wordpress.com/(\d{4})/0?(\d+)/0?(\d+)/question-\d+/" rel="bookmark">Question (\d+).?</a>',re.I)
 robj=r.findall(web.text)
 dt=datetime.datetime.now()#current date
 for y,m,d,q in robj:
   if (dt-datetime.datetime(int(y),int(m),int(d))).days<=7:
    print("Found new entry: "+"Question "+str(q))
    yield int(q)
##############################################################################

updateinfo()
for i in scrapper():
 createf(i)

updateinfo(1)
getinfo()

 
  
  

