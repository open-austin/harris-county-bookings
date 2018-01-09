# harris-county-bookings

A searchable repository which aggregates the daily Harris County Justice Information and Management System 1058 
reports (JIMS 1058) of arrests from the [Harris County Sheriff's Office](http://home.jims.hctx.net/). 
The latest JIMS 1058 report can be found via the [Harris County JIMS site](http://www.jims.hctx.net/jimshome/jimsreports/jims1058.txt). 
This information is intended for researchers and non-profits looking to do studies on policing in Harris County.

In this public repository, personal information data is removed and the abridged dataset is saved to the 
[`data`](data) directory. Please see [JIMSRecorder#ALL_HEADERS](jims_recorder.py#L27) 
for the latest on which headers are removed. If your research requires the raw data, please contact 
[Open Austin](mailto:info@open-austin.org) for access to 
[open-austin/harris-county-bookings-raw](https://github.com/open-austin/harris-county-bookings-raw). 

## Usage

Install dependencies.

```
pip install -r requirements.txt
```

Get today's _scrubbed_ JIMS 1058 report and save it in the `data` directory.

```
./save_today.py
```

Get today's _raw_ JIMS 1058 report and save it in the `raw-data` directory.

```
./save_today.py --mode raw
```

Get both today's raw and scrubbed JIMS 1058 report and save them in the appropriate directories. 

```
./save_today.py --mode both
```

To get today's JIMS 1058 report and to save it to GitHub, data.world, or S3, first create 
a `harris_county_bookings/settings.py` file and include your account credentials. 
(See `harris_county_bookings/settings_example.py` for an example of the contents.) Then run 
`save_today.py` with the `--commit`, `--dataset`, or `--s3` flag.

The `--mode` flag can be used in combination to suit your needs.

Examples:
```
./save_today.py --commit
./save_today.py --dataset
./save_today.py --s3
./save_today.py --commit --dataset --mode raw
```

### Lambda Usage

1. Create the `harris_county_bookings/settings.py` file as previously mentioned.
2. Configure AWS credentials via the usual means (i.e. `aws configure` or environment variables).
3. Manage the Lambda function.
 * Initial deployment: `invoke clean create_lambda`
 * Subsequent code updates: `invoke clean deploy`

The deployed Lambda function will execute `./save_today.py --commit --dataset --mode both`.

## TODO

- tests

## Context

This project was started thanks to an 
[idea posted Open Austin's project-ideas repo](https://github.com/open-austin/project-ideas/issues/73). 
Please refer tothat for additional context.

## License

The code for this repository has been released into the public domain by Open Austin via the
[Unlicense](http://unlicense.org).
