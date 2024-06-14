# HACKING.md

## About [gpx.skolbacken.com](https://gpx.skolbacken.com)
A simple tool for converting `.gpx` files to text for upload to [artportalen.se](https://artportalen.se) 

### Tech stash overview:
* [FastAPI](https://fastapi.tiangolo.com/) - like regular APIs but also fast
* [jinja2](https://jinja.palletsprojects.com/) - {{ funny_description|censor_words }}
* [Hatchling](https://pypi.org/project/hatchling/) - package build system
* [htmx](https://htmx.org/) - the wheel reinvented for the last time, again
* [Pico css](https://picocss.com/) - unintrusive css framework
* [Fontawesome icons](https://docs.fontawesome.com/web) - the path of least resistance

### Deployment
This repo builds a docker image that is manually deployed on Google Cloud compute. 


## Table of Contents
- [Quickstart](#quickstart)
- [Install](#install)
- [Develop](#develop)
- [Test](#test)
- [Build](#build)
- [Deploy](#deploy)
- [License](#license)

-----

## Quickstart: [`scripts/patience.sh`](scripts/patience.sh)
Convenience script that builds and runs the container.
> **REQUIRES** `docker`

> **ARGUMENTS** `engine`: optional path to container runtime. (Default is "docker")

```
$ scripts/patience.sh [path/to/engine]
```

## Installation
> **REQUIRES** `python` >= 3.10, `pip`

You can install the `gpx2artdata` module and its dependencies using the `pip`. 
```console
$ pip install .
```
If you want to install the api environment, specify the `server` optional dependency group.
> **NOTE** This does not install the actual application, which lives in [`main.py`](main.py)
```console
$ pip install .[server]
```
For development, please use the `[dev]` group and pass the `-e` flag to make the installation ediatable-in-place.
> **TIP** Use a virtual environment [like a sane person](#develop).
```console
$ pip install -e .[dev]
```

## Develop
> **REQUIRES** `python` > 3.10, `pip`

Use [`scripts/dev-setup.sh`](scripts/dev-setup.sh) to set up a local development environment. 

> **IMPORTANT** The script preserves any configuration done in `local.env` but unconditionally torches your `.venv` folder. 

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

    b. Invoke `uvicorn` from the main python script. I find this easier to debug.
    ```console
    (.venv) 
    $ python main.py
    ```

### Runtime environment
> **NOTE** The container server will run in production mode by default. For building and testing locally without a https proxy, set `$PRODUCTION=False`.

- `$PRODUCTION` Disables the documentation endpoints and ensures that all generated URLs are https://
- `$WEBSITE_HOSTNAME` Used for showing link to new URL 
- `$PROTOCOL` (optional) Defaults to https in production mode, but http is used by `dev-server.sh`
- `$STATIC_URL` (optional) Set to fully qualified URL if the `static/` endpoint is served from a different location. This is also needed to ensure https under various proxy setups.
- `$BUILD_VERSION` displays in page footer



### JavaScript and frontend parts
> **WARNING** The `main.js` component is developed ad-hoc by an absolute amateur. Several conflicting best practices are pursued simultaneously. There is no toolchain. Good luck. 

This application relies on [`htmx`](https://htmx.org) for asynchronous requests and DOM patching. There really isn't that much to it. See [`main.py`](main.py): `is_htmx()`.

### Generating `dictionary.js`
> **REQUIRES** API key to [Artdata - Taxon List Service](https://api-portal.artdatabanken.se/api-details#api=taxonlistservice&operation=definitions)

> **NOTE** Do not expect `scripts/update-dictionary.sh` to work, it is outdated. 

[`static/dictionary.js`](static/dictionary.js) contains a list used for auto-suggesting taxon names and spell checking. It is provided mostly as a guideline to help users correct obvious mistakes, there is no guarantee that the output will work at [artportalen.se](https://artportalen.se). 

Functions for fetching and filtering taxon data are in [`scripts/species_list.py`](scripts/species_list.py). Some manual labour will be needed if you want to produce a new dictionary file. 

### Versioning
> **INFO** This package uses [Semantic Versioning](https://semver.org/). 

> **ARGUMENTS** `scripts/bump-version.sh` accepts either a full version string like `1.5.2`, or one of the keywords `major`, `minor` and `patch`. If a second argument is provided it will be used as a description for the new version tag. 

Versioning is provided by `hatch`. Use [`scripts/bump-version.sh`](scripts/bump-version.sh) to generate the [`CHANGELOG.md`](CHANGELOG.md). 


## Test
There is a simple sanity check in the `tests` folder.

## Build
> **REQUIRES** `docker` or `podman` (untested). 

> **ARGUMENTS** `env_file`, path to a .env file. Default is `local.env` 

Use [`scripts/build.sh`](scripts/build.sh) to build a container image. See `local.env.example` for configuration options. 

## Deploy
> **REQUIRES** `gcloud` (Google Cloud platform CLI) and authentication

> **ENVIRONMENT** Copy [`gcloud.env.example`](gcloud.env.example) to `gcloud.env` and edit to match your life situation. 

This repo is configured to build and push a docker image to the Google Cloud/Artifact registry with a minimal amount of Google lock-in bullshit. 

Use [`scripts/gcloud-push.sh`](scripts/gcloud-push.sh) to build and push the image. Configuring the required Google Cloud Artifact registry is beyond the scope of this guide. I found this [article](https://medium.com/@taylorhughes/how-to-deploy-an-existing-docker-container-project-to-google-cloud-run-with-the-minimum-amount-of-daca0b5978d8) helpful. 

> **NOTES** on `gcloud-push.sh`
> 
> - Aborts if the repo is not clean-ish.
> - The default entrypoint (`server.sh`) runs the server with `--proxy-headers`. The reason is [this](https://www.googlecloudcommunity.com/gc/Serverless/Containerized-FastAPI-app-using-Uvicorn-serving-JS-amp-CSS/m-p/681551).
> - For the same reason the `WEBSITE_URL` is required at container build time. This hard-codes the `/static` endpoint so it serves https, as the gods intended.   
> - If the script is run with *any* argument it will just build the container. IDK just so you know.


## License

`gpx2artdata` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
