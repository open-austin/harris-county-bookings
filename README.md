# harris-county-bookings

A searchable repository of the daily Harris County Justice Information and Management System 1058 reports (JIMS 1058).
The latest JIMS 1058 report can be found at http://www.jims.hctx.net/jimshome/jimsreports/jims1058.txt

## Usage

Install dependencies.

```
pip install -r requirements.txt
```

Get today's JIMS 1058 report and save it in the `data` directory.

```
./save_today.py
```

To get today's JIMS 1058 report and and save it as a commit in a GitHub repository, first create a
`harris_county_bookings/settings.py` file containing your GitHub information. (See
`harris_county_bookings/settings_example.py` for an example of the contents.) Then run `save_today.py` with the
`--commit` flag.

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

## TODO

- tests

## Context

This project was started thanks to an 
[idea posted Open Austin's project-ideas repo](https://github.com/open-austin/project-ideas/issues/73). Please refer to
that for additional context.

## License

The code for this repository has been released into the public domain by Open Austin via the
[Unlicense](http://unlicense.org).
