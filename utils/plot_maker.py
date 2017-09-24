import sys, os 
import numpy as np 
import seaborn as sns
import matplotlib.pylab as plt
import date_funcs as datef



def make_date_user_plot(mydf, user_name,bfa = True):
    '''
    input: mydf and usuername 
        - we want user name incase we have a combined dataframe with multiple people
        - flag for before and after 
    returns: a plot colored with before and after ig change by default 
    '''

    firstday, abs_day, turn_day, dnlikes = datef.user_date_model(mydf)

    pre_day = [abs_day[x] for x in range(len(abs_day)) if abs_day[x] < turn_day]
    pre_likes = [dnlikes[x] for x in range(len(abs_day)) if abs_day[x] < turn_day]
    post_day = [abs_day[x] for x in range(len(abs_day)) if abs_day[x] >= turn_day]
    post_likes = [dnlikes[x] for x in range(len(abs_day)) if abs_day[x] >= turn_day]

    colors = ['b','r']
    if not bfa:
        # make all the same colors
        colors[1]='b'

    ax = sns.regplot(np.asarray(pre_day), np.asarray(pre_likes), fit_reg=False, color='b', marker="+",
                     scatter_kws={"s": 8})
    ax = sns.regplot(np.asarray(post_day), np.asarray(post_likes), fit_reg=False, color='r', marker="+",
                     scatter_kws={"s": 8})
    plt.legend()
    plt.title("Growth number of likes over time \n {}".format(user_name))
    plt.xlabel("Days")
    plt.ylabel("Number Likes")
    plt.show()
    return

def make_ttplot(my_reg, X_train, X_test, y_train, y_test):
    # This will become depreicated eventually. we want to show model resolution as actual-predic
    gg = sns.jointplot(np.asarray(y_train), np.asarray(my_reg.predict(X_train)), kind="reg", color="r", marker='+',
                       size=6)
    gg = sns.jointplot(np.asarray(y_test), np.asarray(my_reg.predict(X_test)), kind="reg", color="b", marker='+',
                        size=6)
    plt.ylabel("Predicted")
    plt.xlabel("Actual")
    plt.show()
    return

