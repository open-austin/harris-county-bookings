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

## TODO

- push to GitHub
- set up the cron (likely via lambda)?

## Context

This project was started thanks to an 
[idea posted Open Austin's project-ideas repo](https://github.com/open-austin/project-ideas/issues/73). Please refer to
that for additional context.

## License

The code for this repository has been released into the public domain by Open Austin via the
[Unlicense](http://unlicense.org).
