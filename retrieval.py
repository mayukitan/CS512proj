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
                  'select '
                    'repository_name,'
                    'repository_owner,'
                    'type,'
                    'YEAR(created_at) as year,'
                    'QUARTER(created_at) as quarter'
                  'from [githubarchive:github.timeline],'
                  'where'
                      'type = 'PushEvent'/'
                      'AND repository_url != '''
                      'AND YEAR(created_at)= 2014'
                      'AND (QUARTER(created_at)=1)'
                  'group by '
                    'repository_name,'
                    'repository_owner,'
                    'type,'
                    'year,'
                    'quarter'
                    )
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
    parser.add_argument('project_id', help='Your Google Cloud Project ID.')

    args = parser.parse_args()

    main(args.project_id)
