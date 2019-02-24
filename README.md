# Sync Trello Slack Status

## Overview

This repository provides a code to reflect your Trello condition (How you are busy) to Slack status using AWS Lambda.

## How to deploy

### 1) Create a zip archive

```
$ git clone https://github.com/shinobe179/sync-trello-slack-status.git
$ cd sync-trello-slack-status
$ pip install -r requirements.txt -t ./
$ zip -r stss.zip .
```

### 2) Upload the zip archive to AWS Lambda

### 3) Set environment variables

### 4) Create an event rule on AWS Cloudwatch as you like
