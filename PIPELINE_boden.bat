@echo off
python cut_equi_top.py -i img/lol.png -o img/sliced_bottom.png
python convert360 --convert e2c --i img/sliced_bottom.png --o img/cubemap.png --w 1520 --mode bilinear
python cubemap_trim_floor.py -i img/cubemap.png -o img/floorfloor.png
pause