"""
These settings are only needed if you are planning to push to S3, GitHub or data.world.
If you only are only saving to local files, then these are not needed.
"""

S3_BUCKETS = {
    # 'bucket': name of the bucket
    # 'key': syntax: a_folder/another_folder
    #
    # For the 'scrub' bucket, one sub-folder named 'data' is created
    # For the 'raw' bucket, two sub-folders are created: 'original-files' & 'raw-data'
    'scrub': {'bucket': 'THE_PUBLIC_BUCKET_TO_SAVE_TO', 'key': 'THE_DIRECTORY_TO_SAVE_TO'},
    'raw': {'bucket': 'THE_PRIVATE_BUCKET_TO_SAVE_TO', 'key': 'THE_DIRECTORY_TO_SAVE_TO'}
}

GITHUB_API_TOKEN = 'YOUR_GITHUB_TOKEN_HERE'
GITHUB_REPOS = {
    # 'name': syntax: repo_owner/repo_name
    'scrub': {'name': 'THE_PUBLIC_REPO_YOU_WANT_TO_PUSH_TO', 'branch': 'THE_BRANCH_YOU_WANT_TO_PUSH_TO'},
    'raw': {'name': 'THE_PRIVATE_REPO_YOU_WANT_TO_PUSH_TO', 'branch': 'THE_BRANCH_YOU_WANT_TO_PUSH_TO'}
}

DATAWORLD_API_TOKEN = 'YOUR_DATAWORLD_TOKEN_HERE'
DATAWORLD_DATASETS = {
    'scrub': {'owner': 'DATASET_OWNER', 'name': 'THE_PUBLIC_DATASET_YOU_WANT_TO_PUSH_TO'},
    'raw': {'owner': 'DATASET_OWNER', 'name': 'THE_PRIVATE_DATASET_YOU_WANT_TO_PUSH_TO'}
}
