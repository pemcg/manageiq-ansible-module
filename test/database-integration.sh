#!/bin/bash
bundle exec kitchen converge database-replicate
bundle exec kitchen converge database-failover
bundle exec kitchen converge database-external
bundle exec kitchen verify "database-(replicate|external|failover)"
bundle exec kitchen destroy -c
