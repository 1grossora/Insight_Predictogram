import os

# The user

user = 'groryangro' # make this an input 

outputdir = '../data/Scraped_Profile/{}'.format(user)

if not os.path.isdir(outputdir):
    os.mkdir(outputdir)


cmd = 'instagram-scraper {} -t image --include-location -d {}/'.format(user,outputdir)
os.system(cmd)
