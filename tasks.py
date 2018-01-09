import os
import shutil
import glob
from invoke import task

from harris_county_bookings.constants import VERSION


@task
def dist(ctx):
    """Build a distribution zip that is intended for AWS Lambda"""

    # Checking to see if you've made a correct harris_county_bookings/settings.py
    # noinspection PyUnresolvedReferences
    from harris_county_bookings.settings import GITHUB_API_TOKEN, GITHUB_REPOS, \
        DATAWORLD_API_TOKEN, DATAWORLD_REPOS

    dist_root_dir = 'dist'
    dist_dir = '{}/harris_county_bookings'.format(dist_root_dir)
    dist_zip = 'harris_county_bookings-{}.zip'.format(VERSION)
    mkdir(dist_root_dir)
    mkdir(dist_dir)

    print('Installing dependencies to {}'.format(dist_root_dir))
    ctx.run('pip install -q -r requirements.txt -t {}'.format(dist_root_dir))

    print('Copying source code to {}'.format(dist_root_dir))
    ctx.run('cp save_today.py {}'.format(dist_root_dir))
    for python_file in glob.glob('harris_county_bookings/*.py'):
        ctx.run('cp {} {}'.format(python_file, dist_dir))

    print('Zipping package into {}'.format(dist_zip))
    ctx.run('cd {} && zip -9qr ../{} ./*'.format(dist_root_dir, dist_zip))


@task(dist)
def create_lambda(ctx):
    """One-time task to create the AWS Lambda function"""
    dist_zip = 'harris_county_bookings-{}.zip'.format(VERSION)
    name = 'harris_county_bookings-{}'.format((VERSION.replace('.', '_')))
    
    print('Creating AWS Lambda function {} with {}'.format(name, dist_zip))
    cmd = ('aws lambda create-function --function-name {}'
           ' --zip-file fileb://{} --handler save_today.lambda_handler'
           ' --runtime python3.6 --role arn:aws:iam::994940854184:role/lambda_basic_execution'
           ' --timeout 300 --description "Function to pull Harris County JIMS 1058 reports"')
    ctx.run(cmd.format(name, dist_zip))


@task(dist)
def deploy(ctx):
    """Deploy code to the AWS Lambda function"""
    dist_zip = 'harris_county_bookings-{}.zip'.format(VERSION)
    name = 'harris_county_bookings-{}'.format(VERSION.replace('.', '_'))

    print('Updating AWS Lambda function {} with {}'.format(name, dist_zip))
    cmd = 'aws lambda update-function-code --function-name {} --zip-file fileb://{}'
    ctx.run(cmd.format(name, dist_zip))


@task
def clean(ctx):
    """Clean the dist dir and the distribution zip"""
    dist_dir = 'dist'
    dist_zip = 'harris_county_bookings-{}.zip'.format(VERSION)

    if os.path.exists(dist_dir):
        shutil.rmtree(dist_dir)

    if os.path.exists(dist_zip):
        os.remove(dist_zip)

    for pyc_file in glob.glob('harris_county_bookings/*.pyc'):
        os.remove(pyc_file)


def mkdir(dir_name):
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
