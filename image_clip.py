from pathlib import Path

import click
from PIL import Image


SUPPORTED_FORMATS = {".png", ".jpg", ".jpeg"}


def format_kb(size_bytes: int) -> str:
    size_kb = size_bytes / 1024
    return f"{size_kb:.0f}KB"


def center_crop(image: Image.Image, target_width: int, target_height: int) -> Image.Image:
    if target_width > image.width or target_height > image.height:
        raise ValueError(
            "Target size must be less than or equal to input size for cropping."
        )

    left = (image.width - target_width) // 2
    top = (image.height - target_height) // 2
    right = left + target_width
    bottom = top + target_height

    return image.crop((left, top, right, bottom))


@click.command()
@click.argument("input_path", type=click.Path(exists=True, dir_okay=False, path_type=Path))
@click.argument("output_path", type=click.Path(dir_okay=False, path_type=Path))
@click.option("--width", "target_width", required=True, type=int)
@click.option("--height", "target_height", required=True, type=int)
def clip_resize(input_path: Path, output_path: Path, target_width: int, target_height: int) -> None:
    """Resize by clipping equally from each side to center the composition."""
    if input_path.suffix.lower() not in SUPPORTED_FORMATS:
        raise click.ClickException("Input format must be PNG, JPG, or JPEG.")
    if output_path.suffix.lower() not in SUPPORTED_FORMATS:
        raise click.ClickException("Output format must be PNG, JPG, or JPEG.")

    input_size = input_path.stat().st_size

    try:
        with Image.open(input_path) as image:
            cropped = center_crop(image, target_width, target_height)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            cropped.save(output_path)
            input_dimensions = (image.width, image.height)
    except ValueError as exc:
        raise click.ClickException(str(exc)) from exc

    output_size = output_path.stat().st_size

    click.echo(f"Input size: {input_dimensions[0]}x{input_dimensions[1]}")
    click.echo(f"Input file size: {format_kb(input_size)}")
    click.echo(f"Output size: {target_width}x{target_height}")
    click.echo(f"Output file size: {format_kb(output_size)}")
    click.echo(f"Path: {output_path}")


if __name__ == "__main__":
    clip_resize()
