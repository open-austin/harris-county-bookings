"""
These settings are only needed if you are planning to push to GitHub or publish to data.world.
If you only are only saving to local files, then these are not needed.
"""

GITHUB_API_TOKEN = 'YOUR_GITHUB_TOKEN_HERE'
GITHUB_REPOS = {
    # 'name' requires the following syntax: repo_owner/repo_name
    'scrub': {'name': 'THE_PUBLIC_REPO_YOU_WANT_TO_PUSH_TO', 'branch': 'THE_BRANCH_YOU_WANT_TO_PUSH_TO'},
    'raw': {'name': 'THE_PRIVATE_REPO_YOU_WANT_TO_PUSH_TO', 'branch': 'THE_BRANCH_YOU_WANT_TO_PUSH_TO'}
}

DATAWORLD_API_TOKEN = 'YOUR_DATAWORLD_TOKEN_HERE'
DATAWORLD_DATASETS = {
    'scrub': {'owner': 'DATASET_OWNER', 'name': 'THE_PUBLIC_DATASET_YOU_WANT_TO_PUSH_TO'},
    'raw': {'owner': 'DATASET_OWNER', 'name': 'THE_PRIVATE_DATASET_YOU_WANT_TO_PUSH_TO'}
}
