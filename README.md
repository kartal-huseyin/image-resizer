# zed-base

## Image clipping CLI

Use the CLI to crop images by clipping equally from all four sides to maintain a centered composition.

```1:1:image_clip.py
python image_clip.py image1.jpg image2.png image3.jpeg --target 100:100
```

For a single input, you can also supply `--output`:

```1:1:image_clip.py
python image_clip.py input.jpg --target 180:100 --output output.jpg
```

If you omit `--output`, the CLI saves files under `./output/` using the format
`output_{name}_{width}x{height}_{timestamp}.{ext}`.

Example progress output:

```1:1:image_clip.py
✓ Processed image1.jpg → output_image1_100x100_20250225_103045.jpg
✓ Processed image2.png → output_image2_100x100_20250225_103045.png
✓ Processed image3.jpeg → output_image3_100x100_20250225_103045.jpeg
```