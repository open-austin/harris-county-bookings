import os
import shutil
import glob
from invoke import task

from harris_county_bookings.constants import VERSION


@task
def dist(ctx):
    """Build a distribution zip that is intended for AWS Lambda"""
    # noinspection PyUnresolvedReferences
    # checking to see if you've made a correct harris_county_bookings/settings.py
    from harris_county_bookings.settings import GITHUB_API_TOKEN, GITHUB_BRANCH, GITHUB_REPO_NAME

    dist_root_dir = 'dist'
    dist_dir = '%s/harris_county_bookings' % dist_root_dir
    dist_zip = 'harris_county_bookings-%s.zip' % VERSION
    mkdir(dist_root_dir)
    mkdir(dist_dir)

    print('Installing dependencies to %s' % dist_root_dir)
    ctx.run('pip install -q -r requirements.txt -t %s' % dist_root_dir)

    print('Copying source code to %s' % dist_root_dir)
    ctx.run('cp save_today.py %s' % dist_root_dir)
    for python_file in glob.glob('harris_county_bookings/*.py'):
        ctx.run('cp %s %s' % (python_file, dist_dir))

    print('Zipping package into %s' % dist_zip)
    ctx.run('cd %s && zip -9qr ../%s ./*' % (dist_root_dir, dist_zip))


@task(dist)
def create_lambda(ctx):
    """One-time task to create the AWS Lambda function"""
    dist_zip = 'harris_county_bookings-%s.zip' % VERSION
    print('Creating the AWS Lambda function for %s' % dist_zip)
    cmd = ('aws lambda create-function --function-name harris_county_bookings'
           ' --zip-file fileb://%s --handler save_today.lambda_handler'
           ' --runtime python2.7 --role arn:aws:iam::153011574665:role/lambda_basic_execution'
           ' --timeout 300 --description "Function to pull Harris County JIMS 1058 reports"')
    ctx.run(cmd % dist_zip)


@task(dist)
def deploy(ctx):
    """Deploy code to the AWS Lambda function"""
    dist_zip = 'harris_county_bookings-%s.zip' % VERSION
    print('Updating the AWS Lambda function with %s' % dist_zip)
    cmd = 'aws lambda update-function-code --function-name harris_county_bookings --zip-file fileb://%s'
    ctx.run(cmd % dist_zip)


@task
def clean(ctx):
    """Clean the dist dir and the distribution zip"""
    dist_dir = 'dist'
    dist_zip = 'harris_county_bookings-%s.zip' % VERSION
    if os.path.exists(dist_dir):
        shutil.rmtree(dist_dir)
    if os.path.exists(dist_zip):
        os.remove(dist_zip)
    for pyc_file in glob.glob('harris_county_bookings/*.pyc'):
        os.remove(pyc_file)


def mkdir(dir_name):
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
