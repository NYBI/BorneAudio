#!/bin/bash

# monter la clef USB
mount /dev/sda /mnt/clef

# jouer la piste
mpg123 "$(find /mnt/clef -name \*.mp3 | shuf -n 1)"
#find /mnt/clef -name \*.mp3 | shuf -n 1

#find /mnt/clef -name *.mp3 | shuf -n 1

# demonter la clef USB
umount /mnt/clef

