#TODO: Add a Dockerfile for the build process
#Syntax: docker build
#start image with a node application
FROM node:18-alpine as builder-stage
# create an application directory
RUN mkdir -p /app
WORKDIR /app

# run recognition.py