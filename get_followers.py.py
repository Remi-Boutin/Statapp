#encoding: utf-8

import tweepy
import time
import os
import sys
import json
import argparse

try :
	os.mkdir('twitter-users/')
except OSError as e:
    if e.errno != errno.EEXIST:
        raise

FOLLOWING_DIR = 'following'
MAX_FRIENDS = 100
FRIENDS_OF_FRIENDS_LIMIT = 100

if not os.path.exists(FOLLOWING_DIR):
    os.mkdir(FOLLOWING_DIR)

enc = lambda x: x.encode('ascii', errors='ignore')

# The consumer keys can be found on your application's Details
# page located at https://dev.twitter.com/apps (under "OAuth settings")
CONSUMER_KEY = #############################
CONSUMER_SECRET = ##########################
# The access tokens can be found on your applications's Details
# page located at https://dev.twitter.com/apps (located
# under "Your access token")
ACCESS_TOKEN = ##############################
ACCESS_TOKEN_SECRET = ########################


# == OAuth Authentication ==
#
# This mode of authentication is the new preferred way
# of authenticating with Twitter.
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

api = tweepy.API(auth)

def get_follower_ids(centre, max_depth=1, current_depth=0, taboo_list=[]):

    print 'current depth: %d, max depth: %d' % (current_depth, max_depth)
    print 'taboo list: ', ','.join([ str(i) for i in taboo_list ])

    if current_depth == max_depth:
        print 'out of depth'
        return taboo_list

    if centre in taboo_list:
        # we've been here before
        print 'Already been here.'
        return taboo_list
    else:
        taboo_list.append(centre)

    try:
        userfname = os.path.join('twitter-users/'+ str(centre) + '.json')
        if not os.path.exists(userfname):
            print 'Retrieving user details for twitter id %s' % str(centre)
            while True:
                try:
                    user = api.get_user(centre)

                    d = {'name': user.name,
                         'screen_name': user.screen_name,
                         'id': user.id,
                         'friends_count': user.friends_count,
                         'followers_count': user.followers_count,
                         'followers_ids': user.followers_ids()}

                    with open(userfname, 'w') as outf:
                        json.dump(d, outf, indent=1)

                    user = d
                    break
                except tweepy.TweepError, error:
                    print type(error)

                    if str(error) == 'Not authorized.':
                        print 'Can''t access user data - not authorized.'
                        return taboo_list

                    if str(error) == 'User has been suspended.':
                        print 'User suspended.'
                        return taboo_list

                    errorObj = error[0][0]

                    print errorObj

                    if errorObj['message'] == 'Rate limit exceeded':
                        print 'Rate limited. Sleeping for 15 minutes.'
                        time.sleep(15 * 60 + 15)
                        continue

                    return taboo_list
        else:
            user = json.loads(file(userfname).read())

        screen_name = enc(user['screen_name'])
        #fname = os.path.join(FOLLOWING_DIR, screen_name + '.csv')
        friendids = []

        friendids=d['followers_ids']
        # get friends of friends
        cd = current_depth
        if cd+1 < max_depth:
            for fid in friendids[:FRIENDS_OF_FRIENDS_LIMIT]:
                taboo_list = get_follower_ids(fid, max_depth=max_depth,
                    current_depth=cd+1, taboo_list=taboo_list)

        if cd+1 < max_depth and len(friendids) > FRIENDS_OF_FRIENDS_LIMIT:
            print 'Not all friends retrieved for %s.' % screen_name

    except Exception, error:
        print 'Error retrieving followers for user id: ', centre
        print error

        if os.path.exists(fname):
            os.remove(fname)
            print 'Removed file "%s".' % fname

        sys.exit(1)

    return taboo_list

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-s", "--screen-name", required=True, help="Screen name of twitter user")
    ap.add_argument("-d", "--depth", required=True, type=int, help="How far to follow user network")
    args = vars(ap.parse_args())

    twitter_screenname = args['screen_name']
    depth = int(args['depth'])

    if depth < 1 or depth > 3:
        print 'Depth value %d is not valid. Valid range is 1-3.' % depth
        sys.exit('Invalid depth argument.')

    print 'Max Depth: %d' % depth
    matches = api.lookup_users(screen_names=[twitter_screenname])

    if len(matches) == 1:
        print get_follower_ids(matches[0].id, max_depth=depth)
    else:
	print 'Sorry, could not find twitter user with screen name: %s' % twitter_screenname
