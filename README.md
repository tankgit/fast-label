## Fast Labeling tool

used for labeling on images or videos, support jump2frame.

### Environment

- python3.5
- ~~openCV3.1~~
- imageio
- ffmpeg

if you are using anaconda3, just do as follow:

```bash
sudo pip install imageio
sudo pip install ffmpeg
```

### Support media file type

- Image: 
    - *.jpg 
    - *.png
    - *.bmp
- Video:
    - *.avi
    - *.mp4
    - *.wmv
    - *.mkv

### Output file

- Open an single image:`[Image Name].json` saved in the same path with the image.
- Open an video: Create a new directory named `[Video Name]-labels` in the same path with the video, and same frame labels as `[Frame Index].json` in the folder.

- Each time you open an file or a folder, the tool will try to load json file(if exists) 

### Full hotkeys control

You can use keyboard to finish most of operations.

- In main window:
    - `a`: previous frame/image (active in video file or a folder)
    - `d`: next frame/image (active in video file or a folder)
    - `s`: save label file of current frame/image
    - `q + [Num] + [Space]`: choose a new label to draw
        - example: press keys as follow `q[2][space]` to select the 2nd label from label box and add it to image.
        - you can't input any characters but numbers.
    - `w + [Num] + [Space]`: choose an added label as current working label.
    - `e`: edit current working label(rename)
    - `r`: remove current working label.

- In "add label" window:
    - `[ESC]`: cancel
    - `[Return]`: make a new line
    - `[Control] + [Return]`: comfirm to add labels

- In "edit label" window:
    - `[ESC]`: cancel
    - `[Control] + [Return]`: comfirm to rename labels


---
GNU General Public License v3.0