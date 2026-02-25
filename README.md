# zed-base

## Image clipping CLI

Use the CLI to crop images by clipping equally from all four sides to maintain a centered composition.

```1:1:image_clip.py
python image_clip.py input.jpg output.jpg --width 180 --height 100
```

The CLI prints a summary after processing:

```1:1:image_clip.py
Input size: 300x250
Input file size: 50KB
Output size: 180x100
Output file size: 45KB
Path: /output/output.jpg
```