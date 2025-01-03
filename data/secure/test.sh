#! /bin/sh


for i in `ls | grep secur.*[0-9e]$`
do
	`mv $i $i.log`
done
