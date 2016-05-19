# Docker service reporter library 

This is a docker image intended as a base layer for things interacting with my
[service reporter container](https://github.com/csmith/docker-service-reporter).

It provides a python library for interacting with etcd, with convenience
functions for retrieving the higher-level data structures (such as containers
and labels) that the reporter service creates.

## Tests [![CircleCI](https://circleci.com/gh/csmith/docker-service-reporter-lib.svg?style=svg)](https://circleci.com/gh/csmith/docker-service-reporter-lib)

A separate Dockerfile for tests is located in the tests directory. It depends
on a 'dev' label of csmith/service-reporter-lib. There's a docker compose file
to build them together:

```
cd test
docker-compose build
docker-compose run tests
```

