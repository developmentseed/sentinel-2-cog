# sentinel2 to COGEO

Use AWS Lambda and [rio-cogeo](github.com/cogeotiff/rio-cogeo) to convert Sentinel-2 JPEG2000 to CloudOptimized GeoTIFF.

## Deployment

#### Package Lambda

Create `package.zip`

```bash
$ docker-compose build --no-cache
$ docker-compose run --rm package
```

#### Deploy to AWS

```bash
$ npm install
$ sls deploy --bucket my-output-bucket
```

## Use

A CLI is porvided within this repo to invoke the lambda function directly. 

```bash
$ python scripts/invoke.py --help
Usage: invoke.py [OPTIONS] SCENEID

  Invoke Lambda.

Options:
  -b, --bidx TEXT  Band index to copy  [required]
  --stage TEXT     Stack stage
  --function TEXT  Function's name
  --region TEXT    AWS Lambda region
  --help           Show this message and exit.
```

sentinel-2-cog works with Sentinel scene id as defined by [rio-tiler](https://github.com/cogeotiff/rio-tiler/blob/master/rio_tiler/sentinel2.py#L40-L67) 

### Example
```bash
$ python scripts/invoke.py S2B_tile_20190421_18TXR_0 --bidx 04 --bidx 03 --bidx 02
```

## Cost

Each band is processed in ~40Sec, meaning that if you want to process 1M scenes with 4 bands (04, 03, 02, 08) it should cost you around 11$ + the datatransfer (writing to S3).

## Contribution & Development

Issues and pull requests are more than welcome.

**Dev install & Pull-Request**

```
$ git clone http://github.com/developmentseed/sentinel-2-cog.git
$ cd sentinel-2-cog
$ pip install -e .[dev]
```


**Python >=3.6 only**

This repo is set to use `pre-commit` to run *flake8*, *pydocstring* and *black* ("uncompromising Python code formatter") when committing new code.

```
$ pre-commit install
$ git add .
$ git commit -m'my change'
black....................................................................Passed
Flake8...................................................................Passed
Verifying PEP257 Compliance..............................................Passed
$ git push origin
```


## About
Created by [Development Seed](<http://developmentseed.org>)
