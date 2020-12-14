#!/bin/bash

grep '^Date:' | grep -Eo ".[0-9]{4}$" | sort -n | uniq -c | awk '{print $2,$1}'


