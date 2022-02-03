#!/bin/bash
set -e

flacdir=/flash/telemetry/hydrophone
/usr/bin/amixer sset ADC 40db
hostname=$HOSTNAME
mkdir -p $flacdir
timestamp=$(date +%s%3N)
flacout=$hostname-$timestamp-hydrophone.flac
arecord -q -D sysdefault -r 44100 -d 600 -f S16 -V mono - | ffmpeg -i - -y -ac 1 -ar 16000 -sample_fmt s16 $flacdir/.$flacout
mv $flacdir/.$flacout $flacdir/$flacout
sleep 10