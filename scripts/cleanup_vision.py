import sys, os
import json
import requests

# my key

### Add your own key! Don't use mine
#mykey ='XXXXXXXXXXXXXXGOGETAKEYXXXXXXXXXXXXXXXX'

cwd = os.getcwd()
user = 'groryangro'
uservisdir = '{}/../data/Vision/{}/'.format(cwd,user)
usercleandir = '{}/../data/Clean_Vision/{}/'.format(cwd,user)
if not os.path.isdir(usercleandir):
        os.mkdir(usercleandir)

for line in os.listdir(uservisdir):
    cleanjson = usercleandir+line
    if os.path.isfile(cleanjson):
        continue
    #print line
    vispath = '{}{}'.format(uservisdir, line)
    #print vispath
    data = open(vispath, 'rb').read()

    response = requests.post(url='https://vision.googleapis.com/v1/images:annotate?key={}'.format(mykey),data=data,headers={'Content-Type': 'application/json'})

    mynewjson =json.loads(response.text)
    print cleanjson
    with open('{}'.format(cleanjson), 'w') as f:
        json.dump(mynewjson, f)
