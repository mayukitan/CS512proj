
import argparse

from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.client import GoogleCredentials


def main(project_id):
    # Grab the application's default credentials from the environment.
    credentials = GoogleCredentials.get_application_default()
    # Construct the service object for interacting with the BigQuery API.
    bigquery_service = build('bigquery', 'v2', credentials=credentials)

    try:
        query_request = bigquery_service.jobs()
        query_data = {
            'query': (
                  """SELECT repository_name,
                    repository_owner,
                    type
                  FROM [gitcopy.2014_1]
                  WHERE type CONTAINS "PushEvent"
                  GROUP BY repository_name,
                    repository_owner,
                    type;""")
        }

        query_response = query_request.query(
            projectId=project_id,
            body=query_data).execute()

        print('Query Results:')
        for row in query_response['rows']:
            print('\t'.join(field['v'] for field in row['f']))
    
    
    except HttpError as err:
        print('Error: {}'.format(err.content))
        raise err


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('project_id')

    args = parser.parse_args()

    main(args.project_id)












