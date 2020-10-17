#!/bin/bash
while true
do
    python main.py
    sleep 10m
    pgrep chrome | xargs kill -s 9
    pgrep Xvfb | xargs kill -s 9
done
