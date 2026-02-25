# zed-base

## Image clipping CLI

Use the CLI to crop images by clipping equally from all four sides to maintain a centered composition.

```1:1:image_clip.py
python image_clip.py input.jpg --target 180:100 --output output.jpg
```

If you omit `--output`, the CLI saves the file under `./output/` using the format
`output_{width}x{height}_{timestamp}.jpg`.

The CLI prints a summary after processing:

```1:1:image_clip.py
Input size: 300x250
Input file size: 50KB
Output size: 180x100
Output file size: 45KB
Path: /output/output.jpg
```