import time
from slackclient import SlackClient
from pprint import pprint
from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
KEY_FILE_LOCATION = 'ManualRedEye-175393521760.json'
VIEW_ID = '143249669'

#Never Open
def initialize_analyticsreporting():
  """Initializes an Analytics Reporting API V4 service object.

  Returns:
    An authorized Analytics Reporting API V4 service object.
  """
  credentials = ServiceAccountCredentials.from_json_keyfile_name(
      KEY_FILE_LOCATION, SCOPES)

  # Build the service object.
  analytics = build('analytics', 'v4', credentials=credentials)

  return analytics
#Never Open
def get_report(analytics):
  """Queries the Analytics Reporting API V4.

  Args:
    analytics: An authorized Analytics Reporting API V4 service object.
  Returns:
    The Analytics Reporting API V4 response.
  """
  return analytics.reports().batchGet(
      body={
        'reportRequests': [
        {
          'viewId': VIEW_ID,
          'dateRanges': [{'startDate': '7daysAgo', 'endDate': 'today'}],
          'metrics': [{'expression': 'ga:pageviews'}],
          'dimensions': [{'name':'ga:dimension1'}]
        }]
      }
  ).execute()

def money(x):
    money = x
    final = ''
    check = False
    step = 0
    for x in money:
        if check == True:
            step += 1
        if x == '.':
            final += x
            check = True
        else:
            final += x
        if step == 2:
            break
    return final

def count(metric):
  analytics = initialize_analyticsreporting()
  response = analytics.reports().batchGet(
      body={
        'reportRequests': [
        {
          'viewId': VIEW_ID,
          'dateRanges': [{'startDate': '7daysAgo', 'endDate': 'today'}],
          'metrics': [{'expression': 'ga:{}'.format(metric)}],
          #'dimensions': [{'name':'ga:dimension1'}]
        }]
      }
  ).execute()
  pprint(response)
  answer = response['reports'][0]['data']['totals'][0]['values'][0]
  return answer

def user_pageviews(search, metric):
    analytics = initialize_analyticsreporting()
    response = analytics.reports().batchGet(
      body={
        'reportRequests': [
        {
          'viewId': VIEW_ID,
          'dateRanges': [{'startDate': '7daysAgo', 'endDate': 'today'}],
          'metrics': [{'expression': 'ga:{}'.format(metric)}],
          'dimensions': [{'name':'ga:dimension1'}]
        }]
      }
    ).execute()
    answer = response['reports'][0]['data']['rows']
    for step in range(0, len(answer)):
        if answer[step]['dimensions'][0].lower() == search:
            return answer[step]['metrics'][0]['values'][0]
            return '{} has {} pageviews in the last 7 days!'.format(
                answer[step]['dimensions'][0],
                answer[step]['metrics'][0]['values'][0]
            )
        else:
            pass
        #print(answer[step]['dimensions'][0])
        #print(answer[step]['metrics'][0]['values'][0])

# starterbot's ID as an environment variable
BOT_ID = "U6871BMRP"

# constants
AT_BOT = "<@" + BOT_ID + ">"
EXAMPLE_COMMAND = "test"

# instantiate Slack & Twilio clients
slack_client = SlackClient('xoxb-212239395873-ef7jXWTZ9zLiuSJqdUUwYTCn')


def handle_command(command, channel):
    """
        Receives commands directed at the bot and determines if they
        are valid commands. If so, then acts on the commands. If not,
        returns back what it needs for clarification.
    """
    response = "Not sure what you mean. Use the *" + EXAMPLE_COMMAND + \
               "* command with numbers, delimited by spaces."

    if command.startswith(EXAMPLE_COMMAND):
        response = "Sure...write some more code then I can do that!"

    elif command.split()[0] == 'count':
        try:
            metric = command.split()[1]
            print(metric)
            if metric == 'pageviews':
                response = '`{} pageviews in the past 7 days!`'.format(count(metric))
            elif metric == 'sessions':
                response = '`{} sessions in the past 7 days!`'.format(count(metric))
            elif metric == 'adsenserevenue':
                final = money(count(metric))
                response = '`' \
                           '${} Dollars grown on a tree!`'.format(final)
            else:
                response = 'Something broke'

        except HttpError:
            response = 'Sorry, I couldn\'t count `{}`\nTry pageviews, sessions, adsenserevenue.'.format(command.split()[1])

    elif command.split()[0] == 'user':
        metric = command.split()[1]
        user = ' '.join(command.split()[2:])
        if metric == 'pageviews':
            response = '{} has {} page views!'.format(user, user_pageviews(search=user, metric=metric))
        elif metric == 'sessions':
            response = '{} has {} sessions!'.format(user, user_pageviews(search=user, metric=metric))
        elif metric == 'adsenserevenue':
            response = '{} has made ${} moneys'.format(user, money(user_pageviews(search=user, metric=metric)))

    elif command.split()[0] == 'help':
        response = 'Count pageviews / sessions / adsenserevenue \nUser [firstName lastName] pageviews / sessions / adsenserevenue'


    slack_client.api_call("chat.postMessage", channel=channel,
                          text=response, as_user=True)


def parse_slack_output(slack_rtm_output):
    """
        The Slack Real Time Messaging API is an events firehose.
        this parsing function returns None unless a message is
        directed at the Bot, based on its ID.
    """
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text']:
                # return text after the @ mention, whitespace removed
                return output['text'].split(AT_BOT)[1].strip().lower(), \
                       output['channel']
    return None, None


if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print("StarterBot connected and running!")
        while True:
            command, channel = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                handle_command(command, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")

