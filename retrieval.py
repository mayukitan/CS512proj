
import argparse

from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.client import GoogleCredentials


def main(project_id):
    # Grab the application's default credentials from the environment.
    credentials = GoogleCredentials.get_application_default()
    # Construct the service object for interacting with the BigQuery API.
    bigquery_service = build('bigquery', 'v2', credentials=credentials)

""" 
    Pick only top 10 languages
    SELECT TOP(repository_language, 10), COUNT(*)
    FROM [gitcopy.2013]
    WHERE repository_language != " "
"""

    try:
        query_request = bigquery_service.jobs()
        query_data = {
            "allowLargeResults": True,
            'query': (
                  """SELECT repository_name,
                    repository_owner,
                    actor,
                    repository_language
                  FROM [gitcopy.2013]
                  WHERE type CONTAINS 'PullRequestEvent'
                        AND (repository_language CONTAINS "JavaScript"
                        OR repository_language CONTAINS "Ruby"
                        OR repository_language CONTAINS "Python"
                        OR repository_language CONTAINS "Java"
                        OR repository_language CONTAINS "PHP")
                        AND actor != " "
                  GROUP BY repository_name,
                    repository_owner,
                    actor,
                    repository_language;"""
                    )
        }
        query_request2 = bigquery_service.jobs()
        query_data2 = {
            "allowLargeResults": True,
            'query': (
                  """SELECT repository_name,
                    repository_owner,
                    actor,
                    repository_language
                  FROM [gitcopy.2014_2],
                        [gitcopy.2014_3]
                  WHERE type CONTAINS 'PullRequestEvent' 
                        AND (repository_language CONTAINS "JavaScript"
                        OR repository_language CONTAINS "Ruby"
                        OR repository_language CONTAINS "Python"
                        OR repository_language CONTAINS "Java"
                        OR repository_language CONTAINS "PHP")
                        AND repository_language != " "
                        AND actor != " "
                  GROUP BY repository_name,
                    repository_owner,
                    actor,
                    repository_language;"""
                )
            
        }

        query_response = query_request.query(
            projectId=project_id,
            body=query_data).execute()

        with open('training_all.txt', 'w') as f:
            f.write("Training Data (Year 2013)\n")
            s = "repo_name \t repo_owner \t actor \t language\n"
            f.write(s)
            for row in query_response['rows']:
                f.write('\t'.join(field['v'] for field in row['f']) + '\n')

        query_response2 = query_request2.query(
            projectId=project_id,
            body=query_data2).execute()

        with open('ground_truth_all.txt', 'w') as f:
            f.write("Ground Truth\n")
            s = "repo_name \t repo_owner \t actor \t language\n"
            f.write(s)
            for row in query_response2['rows']:
                f.write('\t'.join(field['v'] for field in row['f']) + '\n')

    
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












