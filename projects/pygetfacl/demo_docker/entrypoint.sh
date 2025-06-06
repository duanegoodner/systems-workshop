#!/bin/bash

trap 'true' SIGTERM
tail -f /dev/null &
wait $!