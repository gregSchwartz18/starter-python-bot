"""Hello Analytics Reporting API V4."""
from pprint import pprint
from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials


SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
KEY_FILE_LOCATION = 'ManualRedEye-175393521760.json'
VIEW_ID = '143249669'


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
          'metrics': [{'expression': 'ga:Pageviews'}],
          'dimensions': [{'name': 'ga:country'}, {'name': 'ga:dimension1'}]
        }]
      }
  ).execute()

def past_sessions():
  analytics = initialize_analyticsreporting()
  response = get_report(analytics)
  pprint(response)
  answer = response['reports'][0]['data']['totals'][0]['values'][0]
  return answer

analytics = initialize_analyticsreporting()


print()