# harris-county-bookings

A searchable repository of the daily Harris County Justice Information and Management System 1058 reports (JIMS 1058).
The latest JIMS 1058 report can be found via the 
[Harris County JIMS site](http://www.jims.hctx.net/jimshome/jimsreports/jims1058.txt). This information is intended for
researchers and non-profits looking to do studies on policing in Harris County.

In this public repository, the data is scrubbed of personal information and saved to the `data` directory. If your
research needs the raw data, please contact [Open Austin](https://www.open-austin.org/) for access to
[open-austin/harris-county-bookings-raw](https://github.com/open-austin/harris-county-bookings-raw), which will contain
the raw data in its `raw-data` directory. Verification will be done by Open Austin in order to ensure your research is
legitimate.

The fields that are scrubbed out of the raw data are currently 
`['BOOKING NUMBER', 'NAME', 'DATE OF BIRTH', 'CASE NUMBER']`. Please see 
[JIMSRecorder#ALL_HEADERS](harris-county-bookings/jims_recorder.py#L19) for the latest on which headers are scrubbed
out.

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
./save_today.py --data_mode raw
```

Get both today's raw and scrubbed JIMS 1058 report and dave them in the appropriate directories. 

```
./save_today.py --data_mode both
```

To get today's JIMS 1058 report and and save it as a commit in a GitHub repository, first create a
`harris_county_bookings/settings.py` file containing your GitHub information. (See
`harris_county_bookings/settings_example.py` for an example of the contents.) Then run `save_today.py` with the
`--commit` flag. Use the `--mode` flag in combination to suite your needs.

```
./save_today.py --commit
```

### Lambda Usage

1. Create the `harris_county_bookings/settings.py` as previously mentioned.
2. Configure AWS credentials via the usual means (i.e. `aws configure` or environment variables).
3. Create the Lambda function. This is a one-time task.
```
invoke clean create_lambda
```
4. Deploy any subsequent code updates.
```
invoke clean deploy
```

The deployed Lambda function will be the equivalent of running `./save_today.py --commit --data_mode both`.

## TODO

- tests

## Context

This project was started thanks to an 
[idea posted Open Austin's project-ideas repo](https://github.com/open-austin/project-ideas/issues/73). Please refer to
that for additional context.

## License

The code for this repository has been released into the public domain by Open Austin via the
[Unlicense](http://unlicense.org).
