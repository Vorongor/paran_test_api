#!/bin/bash
awslocal sqs create-queue --queue-name pdf-jobs
awslocal s3 mb s3://user-pdfs