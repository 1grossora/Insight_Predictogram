import sys, os 
import datetime

# This is the magical data that Instagram tried to improve things June, 1, 2016
turn_date = datetime.datetime(2016, 6, 1)

def make_pre_post_algodf(cdf):
    # find the transition date
    pre = cdf[cdf["datetime"]<turn_date]
    post = cdf[cdf["datetime"]>turn_date]
    return pre , post

def user_date_model(mydf):
    '''
    # input: pandas dataframe
    # output:
        - Firstday : First day in date time for the posts
        - absday : list of days relative the to start date on the profile 
        - abs_turn : the day that the algo turns relative to absday 
        - nlikes : number of likes for the given day 
    '''
    # Clean this code up...RG
    nlikes = []
    absday =[]
    kdf_datesort = mydf.sort_values(by='datetime')
    First_day = kdf_datesort["datetime"][len(kdf_datesort)-1]
    abs_turn =-999 # Ugly code... clean up RG  
    # This will be an int relative to the absolute days
    for i, r in kdf_datesort.iterrows():
        theday =r['datetime']
        delta = theday - First_day
        turn_delta = turn_date- theday
        if turn_delta.days <0 and abs_turn==-999:
            abs_turn = delta.days
        absday.append(delta.days)
        nlikes.append(r['Nlikes'])
    return First_day , absday, abs_turn, nlikes
