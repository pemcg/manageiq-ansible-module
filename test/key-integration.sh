#!/bin/bash
bundle exec kitchen converge key-master
bundle exec kitchen converge key-slave
bundle exec kitchen verify "key-(master|slave)"
bundle exec kitchen destroy -c
