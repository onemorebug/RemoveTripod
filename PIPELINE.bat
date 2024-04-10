@echo off
python cut_equi_top.py -i img/original.png -o img/sliced_bottom.png
python convert360 --convert e2c --i img/sliced_bottom.png --o img/cubemap.png --w 1520 --mode bilinear
python cubemap_trim_floor.py -i img/cubemap.png -o img/trimmedfloor.png
python cubemap_glue_floor.py -o img/cubemap-glued.png -c img/cubemap.png -f img/trimmedfloor.png
python convert360 --convert c2e --i img/cubemap-glued.png --o img/equi-whitetop.png --w 6080 --h 3040 --mode bilinear
python glue_images.py --top img/original.png --bottom img/equi-whitetop.png -o img/final.png
pause

