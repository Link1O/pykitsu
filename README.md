# A fast and asynchronous API wrapper for kitsue.io

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/ore0Os/pykitsu/blob/main/LICENCE)
[![Python](https://img.shields.io/badge/python-3.7%2B-blue.svg)](https://www.python.org/downloads/)
[![GitHub issues](https://img.shields.io/github/issues/ore0Os/pykitsu.svg)](https://github.com/ore0Os/pykitsu/issues)
[![GitHub stars](https://img.shields.io/github/stars/ore0Os/pykitsu.svg)](https://github.com/ore0Os/pykitsu/stargazers)
[![discord](https://img.shields.io/badge/discord-join-blue.svg)](https://discord.gg/aFf7TdJdFV)

This is an asynchronous and high-speed Python API wrapper for accessing Kitsu.io API.

## Features

- **Asynchronous**: Utilizes asyncio to perform non-blocking operations, making it efficient for handling multiple requests concurrently.

- **Speed Optimized**: Built to provide fast response times by leveraging efficient HTTP requests.

- **rate limit handled**: comes with a built in rate limit manager.

- **easy to learn**: by simplifying the syntax the library can be really easy to grasp.

## Notes

- **usage**: you can check the examples from [here](https://github.com/ore0Os/pykitsu/blob/main/examples)

## Installation

You can install the library using:

```bash
pip install pykitsu
```

and you can install the requirements using:

```bash
pip install -r https://raw.githubusercontent.com/ore0Os/pykitsu/main/requirements.txt
```

## Version 0.3.0 Patch Notes

### Added
- **get_trending**: Fetches trending items.
- **search_by_id**: Enables specific item search by ID.
- **get_id**: Retrieves the ID for a particular item as a helper tool.

### Removed
- No functionalities were removed in this update.

### Modified
- **Search**: Enhanced the search feature.
- **Random**: Optimized the random feature to provide better results.