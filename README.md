# gpx2artdata: [gpx.skolbacken.com](https://gpx.skolbacken.com)
A simple tool for converting `.gpx` files to text for upload to [artportalen.se](https://artportalen.se) 

## About


## Table of Contents
- [Quickstart](#quickstart)
- [Install](#install)
- [Develop](#develop)
- [Test](#test)
- [Build](#build)
- [Deploy](#deploy)
- [License](#license)

-----

## Quickstart
> **REQUIRES** `docker`

Convenience script that builds and runs a container:
```
$ ./scripts/patience.sh [path/to/container/executable]
```

## Install
> **REQUIRES** Python >= 3.10, pip

You can install the `gpx2artdata` module and its dependencies using the `pip`. 
```console
$ pip install .
```
If you want to install the api environment, specify the `server` optional dependency group.
> **NOTE** This does not install the actual application, which 
```console
$ pip install .
```


## Develop
> **REQUIRES** Python > 3.10, pip

1. Install build dependencies into a new virtual environment:
    ```console
    $ scripts/dev-setup.sh
    ```
2. Use `venv`:
    ```console
    $ source .venv/bin/activate 
    ```
3. Run a development server:
    
    a. Use `fastapi-cli`:
    ```console
    (.venv)
    $ ./dev-server.sh
    ```

    b. Invoke `uvicorn` from the main python script. This is easier to debug.
    ```console
    (.venv) 
    $ python main.py
    ```

### JavaScript parts
It's all vanilla spaghetti by an absolute amateur. Good luck.

### Generating `dictionary.js`
> **REQUIRES** API key

Copy `artdata.env.example` to `artdata.env` and edit with your key for [Artdatabanken Taxonomy](https://api-portal.artdatabanken.se/product#product=taxonomy).

> **NOTE** Do not expect `scripts/update-dictionary.sh` to work, it is work-in-progress.

The `dictionary` is a list used for auto-suggesting taxon names and spell checking.
Functions for fetching and filtering taxon data are in `scripts/species_list.py`.  

## Test
TODO.

## Build
> **REQUIRES** `docker` or `podman` (untested). 

The local `scripts/build.sh` and `scripts/run.sh` accepts an optional `$ENGINE` variable. Default is `docker`.

## Deploy
> **REQUIRES** `gcloud` (Google Cloud platform CLI) and authentication

This repo is configured to build and push a docker image to the Google Cloud/Artifact registry with a minimal amount of Google lock-in bullshit. See `scripts/gcloud-push.sh`

> **NOTES** on `gcloud-push.sh`
> 
> - Will push to the current branch. YOLO :)
> - Aborts if the repo is not clean.
> - A short commit hash will be stored in `templates/githash.txt` and displayed in the footer.
> - The default entrypoint (`server.sh`) runs the server with `--proxy-headers`. The reason is [this](https://www.googlecloudcommunity.com/gc/Serverless/Containerized-FastAPI-app-using-Uvicorn-serving-JS-amp-CSS/m-p/681551).


## License

`gpx2artdata` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
