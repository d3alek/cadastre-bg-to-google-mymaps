#!/bin/bash

echo $1 $2 | cs2cs -r +proj=utm +zone=35 +datum=WGS84 +units=m +no_defs +to +proj=longlat +datum=WGS84 +no_defs -f %.6f
