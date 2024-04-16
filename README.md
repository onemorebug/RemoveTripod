# RemoveTripod
This repository consists of the parent project (RemoveTripod) and 3 git submodules:

1. [Py360Convert](https://github.com/sunset1995/py360convert): 
   Used to convert from equirectangular images to cubemaps and vice versa
2. [Invariant-TemplateMatching](https://github.com/cozheyuanzhangde/Invariant-TemplateMatching):
   Used to locate objects using a template image and a matching mask
3. [Inpaint-Anything](https://github.com/geekyutao/Inpaint-Anything):
   Used to inpaint objects using the coordinates returned from *Invariant-TemplateMatching*
   
The git submodules in the project are forks which have been edited for the project requirements.

## Project setup
### *RemoveTripod*
In directory `RemoveTripod/`:

```bash
pip install -r requirements.txt
```

### *Invariant-TemplateMatching*
In directory `RemoveTripod/Invariant-TemplateMatching/`:
```bash
pip install .
```

### *Inpaint-Anything*
(from *Inpaint-Anything*s README.md)\
Requires `python>=3.8`
```bash
python -m pip install torch torchvision torchaudio
python -m pip install -e segment_anything
python -m pip install -r lama/requirements.txt 
```
In Windows, we recommend you to first install [miniconda](https://docs.conda.io/en/latest/miniconda.html) and
open `Anaconda Powershell Prompt (miniconda3)` as administrator.
Then pip install [./lama_requirements_windows.txt](lama_requirements_windows.txt) instead of
[./lama/requirements.txt](lama%2Frequirements.txt).

Download the model checkpoints provided in [Segment Anything](./segment_anything/README.md) and [LaMa](./lama/README.md) (e.g., [sam_vit_h_4b8939.pth](https://dl.fbaipublicfiles.com/segment_anything/sam_vit_h_4b8939.pth) and [big-lama](https://disk.yandex.ru/d/ouP6l8VJ0HpMZg)), and put them into `./pretrained_models`. For simplicity, you can also go [here](https://drive.google.com/drive/folders/1ST0aRbDRZGli0r7OVVOQvXwtadMCuWXg?usp=sharing), directly download [pretrained_models](https://drive.google.com/drive/folders/1wpY-upCo4GIW4wVPnlMh_ym779lLIG2A?usp=sharing), put the directory into `./` and get `./pretrained_models`.

## Usage 
### Usage with main.py
- [shared-media](shared-media) contains input and output files:
    - ```shared-media/template```: template image for object localization
    - ```shared-media/mask/```: mask matching the template image 
    - ```original.jpg```: original equirectangular image with object to remove
    
- [main.py](main.py) contains the main function which starts the workflow to remove the object. It also contains the file paths which can be set there. 

### Usage from command line
If the execution of the workflow should fail at any point, it is possible to execute most of the steps from the command line:

- Convert equirectangular image to cubemap
```bash
python convert360 --convert e2c --i shared-media/original.jpg --o shared-media/cubemap.png --w 1520 --mode bilinear
```
- Cut out floor tile from cubemap
```bash
python cubemap_trim_floor.py -i shared-media/cubemap.png -o shared-media/floortile.png
```
- Inpaint object at coordinates specified in `--point_coords`
```bash
python remove_anything.py --input_img ./example/remove-anything/candle-floortile.png --coords_type key_in --point_coords 791 768 --point_labels 1 --dilate_kernel_size 15 --output_dir ./results --sam_model_type "vit_h" --sam_ckpt ./pretrained_models/sam_vit_h_4b8939-001.pth --lama_config ./lama/configs/prediction/default.yaml --lama_ckpt ./pretrained_models/big-lama
```

- Insert inpainted floor tile into cubemap
```bash
python cubemap_glue_floor.py -o shared-media/cubemap_inpainted.png -c shared-media/cubemap.png -f shared-media/floortile.png
```
- Convert cubemap to equirectangular image
```bash
python convert360 --convert c2e --i shared-media/cubemap_inpainted.png --o shared-media/final.png --w 6080 --h 3040 --mode bilinear
```



