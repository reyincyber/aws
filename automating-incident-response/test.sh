#!/bin/bash
for j in {1..10}
do
    sudo nmap -sT -Pn 10.X.X.X
done
