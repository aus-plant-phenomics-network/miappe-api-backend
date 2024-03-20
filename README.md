<!-- markdownlint-disable -->
<p align="center">
  <!-- github-banner-start -->
  <!-- github-banner-end -->
</p>
<!-- markdownlint-restore -->

<div align="center">

<!-- prettier-ignore-start -->

| Project |     | Status                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
|---------|:----|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| CI/CD   |     | [![CI](https://github.com/haryle/MIAPPE_API/actions/workflows/ci.yml/badge.svg)](https://github.com/haryle/MIAPPE_API/actions/workflows/ci.yml) [![codecov](https://codecov.io/gh/haryle/MIAPPE_API/graph/badge.svg?token=NQ4AQXLOJF)](https://codecov.io/gh/haryle/MIAPPE_API) [![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=haryle_MIAPPE_API&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=haryle_MIAPPE_API) [![Bugs](https://sonarcloud.io/api/project_badges/measure?project=haryle_MIAPPE_API&metric=bugs)](https://sonarcloud.io/summary/new_code?id=haryle_MIAPPE_API) [![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=haryle_MIAPPE_API&metric=sqale_rating)](https://sonarcloud.io/summary/new_code?id=haryle_MIAPPE_API) |

<!-- prettier-ignore-end -->
</div>

<hr>

## What is this repository about? 

This repository provides an implementation of the [MIAPPE](https://www.miappe.org/) standard for managing plant phenotyping experiments metadata. For practical reasons,
the implemented data model (hence forth referred as MIAPPE+) deviates from the original standard, though we strive to adhere to the original terminologies as much as possible. The high-level schema and 
an example experiment packaged up using MIAPPE+ can be found [here](assets/MIAPPE+_Architecture).

## Meta-usage

If you are a plant scientist who wishes to publish your experiment data, you can either download this tool to run locally, or interact with the APPN hosted metadata server via APIs.
The practical difference between the two options is the amount of data in the catalogue that you have access to. Your local instance likely contains experiment information from only your group, 
but the APPN hosted version contains experiment information from our partner nodes, which enable extensive search capabilities. After packaging up your experiment, you can publish the data to 
a data repository, and the metadata to the ARDC. You also have the option to publish the data to our hosted database after packaging your experiment locally. This allows your experiment to be
discovered by other scientists who use our database catalogue. 

If you are a data pipeline person, you have various options to interact with MIAPPE_API. You can set up a job to export your project metadata to one of our supported formats and upload to the MIAPPE_API database
(either local or remote). More details to come later 

## Usage:
You will first need to install `poetry`:

```bash 
pip install poetry
```

Install the required dependencies: 

```bash 
poetry install 
```

Once finished, you can run the backend server: 
```bash
make dev 
```

Go to `127.0.0.1:8000/schema/swagger` to interact with the backend via APIs.