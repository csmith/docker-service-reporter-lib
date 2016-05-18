# Docker service reporter library 

This is a docker image intended as a base layer for things interacting with my
[service reporter container](https://github.com/csmith/docker-service-reporter).

It provides a python library for interacting with etcd, with convenience
functions for retrieving the higher-level data structures (such as containers
and labels) that the reporter service creates.

