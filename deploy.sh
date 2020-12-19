#!/bin/sh

sam deploy --profile alexa --region us-east-1 \
    --stack-name SmartTVVoiceControl \
    --no-confirm-changeset \
    --s3-bucket aws-sam-cli-managed-default-samclisourcebucket-us-east-1 \
    --s3-prefix SmartTVVoiceControl \
    --capabilities CAPABILITY_IAM --force-upload


sam deploy --profile alexa --region us-west-2 \
    --stack-name SmartTVVoiceControl \
    --no-confirm-changeset \
    --s3-bucket aws-sam-cli-managed-default-samclisourcebucket-us-west-2 \
    --s3-prefix SmartTVVoiceControl \
    --capabilities CAPABILITY_IAM --force-upload

sam deploy --profile alexa --region eu-west-1 \
    --stack-name SmartTVVoiceControl \
    --no-confirm-changeset \
    --s3-bucket aws-sam-cli-managed-default-samclisourcebucket-eu-west-1 \
    --s3-prefix SmartTVVoiceControl \
    --capabilities CAPABILITY_IAM --force-upload
