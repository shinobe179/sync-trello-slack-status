# Sync Trello Slack Status

## Overview

This repository provides a code to reflect your Trello condition (How many tasks you have) to Slack status using AWS Lambda.

## How to deploy

### Prerequires

- Enable to use Trello API.
- Enable to use Slack `users.profile.set` API.

### 1) Create a zip archive

```
$ git clone https://github.com/shinobe179/sync-trello-slack-status.git
$ cd sync-trello-slack-status/src
$ pip install -r requirements.txt -t ./
$ zip -r stss.zip . -x requirements.txt
```

### 2) Upload the zip archive to AWS Lambda

### 3) Set environment variables

- `TRELLO_USERNAME`
    -  username for Trello
- `TRELLO_KEY`
    - API key for Trello
- `TRELLO_TOKEN`
    - API token for Trello
- `IGNORE_LIST_NAME`
    - If there are lists shouldn't be counted(ex. list for done tasks), please registor its name.
- `SLACK_TOKEN`
    - API token for Slack

### 4) Tune timeout value

Default settings is not enough to work correctly. You need to tune(increase) it in most cases.

### 5) Create an event rule on AWS Cloudwatch as you like

To work it automatically. Its interval is as you like.
