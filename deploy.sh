#!/bin/sh

aws cloudformation deploy \
    --profile alexa \
    --stack-name AlexSQSQueue \
    --region us-west-2 \
    --template-file sqs.template.yml \
    --capabilities CAPABILITY_NAMED_IAM CAPABILITY_AUTO_EXPAND CAPABILITY_IAM \
    --no-fail-on-empty-changeset 

AlexaSQSQueueARN=$(
    aws cloudformation list-exports \
        --profile alexa \
        --region us-west-2 \
        --query "Exports[?Name=='AlexaSQSQueueARN'].Value" \
        --out text
)

echo $AlexaSQSQueueARN

sam deploy \
    --profile alexa \
    --region us-east-1 \
    --stack-name SmartTVVoiceControl \
    --template-file lambda.template.yml \
    --no-confirm-changeset \
    --s3-bucket aws-sam-cli-managed-default-samclisourcebucket-us-east-1 \
    --s3-prefix SmartTVVoiceControl \
    --capabilities CAPABILITY_IAM --force-upload \
    --parameter-overrides "ParameterKey=AlexaSQSQueueARN,ParameterValue=$AlexaSQSQueueARN" 

sam deploy \
    --profile alexa \
    --region us-west-2 \
    --stack-name SmartTVVoiceControl \
    --template-file lambda.template.yml \
    --no-confirm-changeset \
    --s3-bucket aws-sam-cli-managed-default-samclisourcebucket-us-west-2 \
    --s3-prefix SmartTVVoiceControl \
    --capabilities CAPABILITY_IAM --force-upload \
    --parameter-overrides "ParameterKey=AlexaSQSQueueARN,ParameterValue=$AlexaSQSQueueARN" 

sam deploy \
    --profile alexa \
    --region eu-west-1 \
    --stack-name SmartTVVoiceControl \
    --template-file lambda.template.yml \
    --no-confirm-changeset \
    --s3-bucket aws-sam-cli-managed-default-samclisourcebucket-eu-west-1 \
    --s3-prefix SmartTVVoiceControl \
    --capabilities CAPABILITY_IAM --force-upload \
    --parameter-overrides "ParameterKey=AlexaSQSQueueARN,ParameterValue=$AlexaSQSQueueARN" 
