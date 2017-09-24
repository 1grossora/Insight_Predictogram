import pandas as pd
import numpy as np
import sys, os
import datetime # time stamps
import json # instagram scraped data is json
import csv  # Needed for social blade data
import emoji # If we want to use emoji finder in text

# lateral imports
#import featfuncs as ff

########################################################
########################################################
# Functions that are used to make and clean data frames
########################################################
########################################################

########################################################
# Bring in the user
########################################################
def make_user_df(user):
    '''
    This function will convert the json to a pandas dataframe
    '''
    mydf = pd.read_json("../data/Scraped_Profile/{}/{}.json".format(user, user))
    return mydf


########################################################
# Clean up the data frame
# RENAME THIS
########################################################
def clean_df2(df):
    '''
    Takes a data frame and cleans it to returna  userful frame
    Note : This is not the frame that contains any of the google vision features
    Returns a clean data set with important colums
    '''

    # # # # # # # # # # # # # # # #
    # add a few useful variables
    # # # # # # # # # # # # # # # #
    mynan = np.nan


    # Keep only image
    mydf = df.copy(deep=True)
    mydf = mydf[(mydf["type"] == 'image') | (mydf["type"] == 'carousel')]

    # Nlikes
    mylikes = []
    for index in mydf["likes"]:
        mylikes.append(index.values()[0])

    # Make a fresh data frame, we will return this frame at the end
    clean_df = pd.DataFrame(np.asarray(mylikes), columns=["Nlikes"])

    # dumb image copy
    myimage =[]
    for index in mydf['images']:
        myimage.append(index.get('standard_resolution'))

    # clean_df["images"] = pd.Series([x for x in myimage])
    clean_df["images"] = [x for x in myimage]

    # User name and ID
    uname = []
    uid = []
    for i in mydf["user"]:
        uname.append(i.values()[0])

    for i in mydf["id"]:
        uid.append(i)

    clean_df["user"] = [x for x in uname]
    clean_df["uid"] = [x for x in uid]

    # Bring in the csv to account for the number of followers
    followers = []

    # Bring in the social blade data
    mycsv = '../data/follower_csv/followers_of_{}.csv'.format(uname[0])
    if not s.path.isfile(mycsv):
        print ' YOU DONT HAVE SOCAIL BLADE DATA... THIS WILL BE FILLED AS NANS'

    with open(mycsv) as f:
        user_follow_dict = dict(csv.reader(f, delimiter=','))

    # Time of post
    mytime = []
    mynan = np.nan
    for index in mydf["created_time"]:
        # convert date time to a string to search in the dict
        date_string = index.strftime('%Y-%m-%d')
        # find the time in the dict
        Nfollowers = user_follow_dict.get(date_string)
        # If it's not in the dict it will be appened as a None so we will fill Nfollowers as NAN
        # We warned you above especially if the file doesnt  exist
        if Nfollowers is None:
            Nfollowers = mynan
        followers.append(Nfollowers)
        mytime.append(index.to_datetime())

    clean_df["nfollowers"] = [float(x) for x in followers]
    clean_df["nfollowers_2"] = [float(x)**2 for x in followers]
    clean_df["nfollowers_3"] = [float(x)**3 for x in followers]
    clean_df["datetime"] = [x for x in mytime]
    clean_df["hour"] = [x.hour for x in mytime]
    clean_df["hour_3"] = [x.hour - x.hour%3  for x in mytime]
    clean_df["year"] = [x.year for x in mytime]
    clean_df["weekday"] = [int(x.weekday()) for x in mytime]
    clean_df["weekday_hr"] = [x.weekday() * 24 + x.hour for x in mytime]

    #def char_is_emoji(character):
    #    return character in emoji.UNICODE_EMOJI

    # Def in Def is ugly but ok for here.
    def text_has_emoji(text):
        for character in text:
            if character in emoji.UNICODE_EMOJI:
                return True
        return False

    # Title
    title_bool = []
    title_emo_bool = []
    title_text_list = []
    title_emo_list = []
    title_text_length = []
    for i in mydf['caption']:
        if i == None:# sometimes there is no caption title. Fill with false and 0
            title_bool.append(False)
            title_emo_bool.append(False)
            title_text_list.append(False)
            title_emo_list.append(False)
            title_text_length.append(0)
            continue

        title_bool.append(True)
        text_length = len(i.get("text").split())  # use split on white space.... count emo as a word
        title_text_length.append(text_length)

        # Check if theres emo
        isemo = text_has_emoji(i.get("text"))
        title_emo_bool.append(isemo)

        # Full Text list
        title_text_list.append("TITLETEXT")
        if isemo:
            title_emo_list.append('MYEMO')# Not used yet...
        else:
            title_emo_list.append("JUNK")# If there are no emojies fill with JUNK wild

    clean_df["has_title"] = [x for x in title_bool]
    clean_df["title_length"] = [x for x in title_text_length]
    clean_df["has_emo"] = [x for x in title_emo_bool]
    clean_df["title_text"] = [x for x in title_text_list]
    clean_df["emo"] = [x for x in title_emo_list]

    # Is this a carousel image set
    iscar = []
    for i in mydf['type']:
        if i == "carousel":
            iscar.append(True)
        else:
            iscar.append(False)

    clean_df["is_car"] = [x for x in iscar] # Does this always work?

    # Location
    ## not using yet but keep for later
    loc_bool = []
    loc_str = []
    for i in mydf['location']:
        if i == None:
            loc_bool.append(False)
            loc_str.append("None")
            continue  # is this needed?
        elif i != i:
            loc_bool.append(False)
            loc_str.append("None")
            continue  # is this needed?
        else:
            loc_bool.append(True)
            loc_str.append(i.values()[0])

    clean_df["is_loc"] = [x for x in loc_bool]
    clean_df["location"] = [x for x in loc_str]

    # Tags AKA known as hashtags
    is_tag = []
    ntag = []
    for i in mydf["tags"]:
        if i != i or len(i) == 0:
            is_tag.append(False)
            ntag.append(0)
        else:
            is_tag.append(True)
            ntag.append(len(i))
    clean_df["is_tag"] = [x for x in is_tag]
    clean_df["ntag"] = [x for x in ntag]

    # Image id
    ph = []
    for i in mydf["images"]:
        mystring = i.values()[0].values()[0]
        ph.append(mystring.rsplit("/", 1)[1])

    clean_df["im_id"] = [x for x in ph]

    # post count Simple dumb index counter
    clean_df["post_count"] = [x for x in range(len(mydf))][::-1]

    return clean_df


########################################################
# Clean up the data frame
########################################################
def make_vision_df(mydf):
    '''
    input: dataframe
    Features we will add
    '''

    # Global vars
    uservisiondir = '../data/Clean_Vision/{}/'.format(mydf["user"][0])

    # Make a copy of things to keep organize
    # frames are not to big so this is fine for now
    fulldf = mydf.copy(deep=True)

    # Get the size of the image
    mydf["images"]
    nface = []  # mnumber of faces
    frac_face = []  # mnumber of faces
    l_JLK = []
    l_SLK = []
    l_ALK = []
    l_SPLK = []
    l_HLK = []
    l_has_face =[]

    LABEL_BLANK = 'UNKNOWN'
    for i, r in mydf.iterrows():

        photo_width = r['images'].get("width")
        photo_height = r['images'].get("height")
        JLK = LABEL_BLANK
        SLK = LABEL_BLANK
        ALK = LABEL_BLANK
        SPLK = LABEL_BLANK
        HLK = LABEL_BLANK
        # Set face to zero
        total_face_area = 0.
        NUMBER_OF_FACE = 0.
        has_face = False # this might not be the best choice

        # Input json that holds the already converted google vision
        tempfile = uservisiondir + r['im_id'].split('.')[0] + '.json'

        if not os.path.isfile(tempfile):# Corupt file # most times these are fine
            l_JLK.append(JLK)
            l_SLK.append(SLK)
            l_ALK.append(ALK)
            l_SPLK.append(SPLK)
            l_HLK.append(HLK)
            l_has_face.append(has_face)
            nface.append(NUMBER_OF_FACE)
            frac_face.append(total_face_area / (photo_width * photo_height))
            continue
        data = open(tempfile, 'rb').read()
        myjson = json.loads(data)
        myvis_dict = myjson.get("responses")[0]

        #if 'labelAnnotations' in myvis_dict and len(myvis_dict.get("labelAnnotations"))==10:
        #    l_Label0.append(myvis_dict.get("labelAnnotations")[0].get('description'))
        #    l_Label1.append(myvis_dict.get("labelAnnotations")[1].get('description'))


        if 'faceAnnotations' in myvis_dict:
            has_face = True
            NUMBER_OF_FACE = len(myjson["responses"][0]["faceAnnotations"])
            # Calculate ratio of face to image
            for face in range(NUMBER_OF_FACE):
                myvertlist = myjson["responses"][0]["faceAnnotations"][face].get("fdBoundingPoly").get("vertices")
                vx = []  # Brain DUMB
                vy = []
                for v in myvertlist:
                    vx.append(v.get("x"))
                    vy.append(v.get('y'))
                # one_face_area = PolyArea(np.asarray(vx),np.asarray(vy))
                vx = np.asarray(vx)
                vy = np.asarray(vy)
                xmax = vx.max()
                xmin = vx.min()
                ymax = vy.max()
                ymin = vy.min()
                if type(xmax) == type(None) or type(ymax) == type(None) or type(xmin) == type(None) or type(
                        ymin) == type(None):
                    continue
                one_face_area = (xmax - xmin) * (ymax - ymin)
                # print one_face_area
                total_face_area += one_face_area

            # Now do the likelihoods of the first face
            JLK = myvis_dict.get("faceAnnotations")[0].get("joyLikelihood")
            SLK = myvis_dict.get("faceAnnotations")[0].get("sorrowLikelihood")
            ALK = myvis_dict.get("faceAnnotations")[0].get("angerLikelihood")
            SPLK = myvis_dict.get("faceAnnotations")[0].get("surpriseLikelihood")
            HLK = myvis_dict.get("faceAnnotations")[0].get("headwearLikelihood")

        l_JLK.append(JLK)
        l_SLK.append(SLK)
        l_ALK.append(ALK)
        l_SPLK.append(SPLK)
        l_HLK.append(HLK)
        l_has_face.append(has_face)
        nface.append(NUMBER_OF_FACE)
        frac_face.append(total_face_area / (photo_width * photo_height))

    fulldf["nfaces"] = [x for x in nface]
    fulldf["face_frac"] = [x for x in frac_face]
    fulldf["JLK"] = [x for x in l_JLK]
    fulldf["SLK"] = [x for x in l_SLK]
    fulldf["ALK"] = [x for x in l_ALK]
    fulldf["SPLK"] = [x for x in l_SPLK]
    fulldf["HLK"] = [x for x in l_HLK]
    fulldf["is_face"] = [x for x in l_has_face]

    return fulldf

