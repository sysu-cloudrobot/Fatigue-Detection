#!/bin/bash 
path_to_data=../data/train
per_class=500

mkdir -p $path_to_data
cd $path_to_data

# current dir is /data/train
for class in *
do 
   class_dir="../validation/$class"
   # created dir /data/train/validation/$class
   mkdir -p $class_dir
   images=$(shuf -n$per_class -e $class/*.jpg )
   for img in $images
   do
       mv $img $class_dir
   done
done

