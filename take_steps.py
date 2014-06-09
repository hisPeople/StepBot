from datetime import datetime, timedelta

__author__ = 'devonmoss'

import fitbit
import pprint


pp = pprint.PrettyPrinter(indent=4)

consumer_key = ''
consumer_secret = ''

user_id = ''
oauth_token = ''
oauth_token_secret = ''

# recreational bball is 138 spm -- a game is 230 spm --
BASKETBALL_SPM = 163
AVG_BBALL_MINS = 45

pedo_steps = [3371, 3693, 5795, 3661, 7804, 13551, 16038]

authd_client = fitbit.Fitbit(consumer_key, consumer_secret, resource_owner_key=oauth_token, resource_owner_secret=oauth_token_secret)

now = datetime.now()
minute = now.minute
hour = now.hour

start_date = datetime(2014, 6, 1)


def calculate_basketball_steps(minutes_played):
    return BASKETBALL_SPM * minutes_played


def log_steps():
    for x, s in enumerate(pedo_steps):
        date_delta = timedelta(days=x)
        new_date = start_date + date_delta
        day = new_date.day
        month = new_date.month
        year = new_date.year

        things = [minute, hour, day, month]

        for t in things:
            if t < 10:
                t = '0' + str(t)
            else:
                t = str(t)

        if new_date.weekday() < 4:
            steps = s + calculate_basketball_steps(AVG_BBALL_MINS)
        else:
            steps = s

        date_string = '{0}-{1}-{2}'.format(year, month, day)
        start_time_string = '{0}:{1}'.format(hour, minute)
        duration = 10234
        activity_data = {'activityId': '90013', 'distanceUnit': 'Steps', 'distance': steps, 'startTime': start_time_string,
                         'durationMillis': duration, 'date': date_string}
        authd_client.log_activity(activity_data)


def get_steps():
    activities_steps = authd_client.time_series('activities/steps', user_id, period='1m')
    return activities_steps


pp.pprint(get_steps())
