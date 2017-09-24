import sys, os 
import subprocess


cwd = os.getcwd()

# Ask the user 
user = 'groryangro'

# Loop through the directory and submit
scrapedir ='../data/Scraped_Profile/{}'.format(user)

for line in os.listdir(scrapedir):
    if line.endswith('json'):
        continue
    myline =  cwd+'/'+scrapedir+'/'+line+' 1:10 4:10 6:1'
    # this give, 1=face , 4=labels, 6= properties, check generate_vision_json.py
    
    imtitle =  line.split(".")[0]

    # Write the file to a text
    thetextfile = '{}/text/user/submit_{}.txt'.format(cwd,user)
    #print thetextfile
    if os.path.isfile(thetextfile):
        os.remove(thetextfile)
    myfile = open(thetextfile,'a+')
    myfile.write(myline+'\n')
    myfile.close()

    # output label
    outlab = '../data/Vision/' + user +'/{}.json'.format(imtitle)

    if not os.path.isdir(outlab.rsplit('/',1)[0]):
        print outlab.rsplit('/',1)[0]
        os.mkdir(outlab.rsplit('/',1)[0])
    # cmd to run process
    cmd = 'python generate_vison_json.py -i {} -o {}'.format(thetextfile,outlab)
    print cmd
    subprocess.call(cmd, shell=True)
