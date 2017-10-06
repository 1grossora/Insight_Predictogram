import os,sys

# The user

#user = 'groryangro' # make this an input 
user = sys.argv[1]
yn = raw_input("Is '{}' the username you want to scrape from Instagram? Y/n \n".format(user))
if yn!='Y':
        # try again 
            sys.exit('Will not scrape')

print 'scrapping {} from Instagram'.format(user)
outputdir = '../data/Scraped_Profile/{}'.format(user)

if not os.path.isdir(outputdir):
    os.mkdir(outputdir)


cmd = 'instagram-scraper {} -t image --include-location -d {}/'.format(user,outputdir)
print cmd

os.system(cmd)

