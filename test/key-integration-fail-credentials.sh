#!/bin/bash
bundle exec kitchen converge key-master
bundle exec kitchen converge key-fail-credentials
bundle exec kitchen destroy -c
