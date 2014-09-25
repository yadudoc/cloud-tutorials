#!/bin/bash

BINDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
$BINDIR/rgb_histogram.pl $1 | sort -rn
