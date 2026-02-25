from datetime import datetime
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


def parse_target(value: str) -> tuple[int, int]:
    if ":" not in value:
        raise click.BadParameter("Target must be in WIDTH:HEIGHT format.")
    width_str, height_str = value.split(":", 1)
    try:
        width = int(width_str)
        height = int(height_str)
    except ValueError as exc:
        raise click.BadParameter("Target dimensions must be integers.") from exc
    if width <= 0 or height <= 0:
        raise click.BadParameter("Target dimensions must be positive integers.")
    return width, height


def build_default_output(target_width: int, target_height: int) -> Path:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"output_{target_width}x{target_height}_{timestamp}.jpg"
    return Path("output") / filename


@click.command()
@click.argument("input_path", type=click.Path(exists=True, dir_okay=False, path_type=Path))
@click.option("--target", "target", required=True, callback=lambda _, __, value: parse_target(value))
@click.option("--output", "output_path", type=click.Path(dir_okay=False, path_type=Path))
def clip_resize(input_path: Path, target: tuple[int, int], output_path: Path | None) -> None:
    """Resize by clipping equally from each side to center the composition."""
    if input_path.suffix.lower() not in SUPPORTED_FORMATS:
        raise click.ClickException("Input format must be PNG, JPG, or JPEG.")

    target_width, target_height = target
    final_output_path = output_path or build_default_output(target_width, target_height)

    if final_output_path.suffix.lower() not in SUPPORTED_FORMATS:
        raise click.ClickException("Output format must be PNG, JPG, or JPEG.")

    input_size = input_path.stat().st_size

    try:
        with Image.open(input_path) as image:
            cropped = center_crop(image, target_width, target_height)
            final_output_path.parent.mkdir(parents=True, exist_ok=True)
            cropped.save(final_output_path)
            input_dimensions = (image.width, image.height)
    except ValueError as exc:
        raise click.ClickException(str(exc)) from exc

    output_size = final_output_path.stat().st_size

    click.echo(f"Input size: {input_dimensions[0]}x{input_dimensions[1]}")
    click.echo(f"Input file size: {format_kb(input_size)}")
    click.echo(f"Output size: {target_width}x{target_height}")
    click.echo(f"Output file size: {format_kb(output_size)}")
    click.echo(f"Path: {final_output_path}")


if __name__ == "__main__":
    clip_resize()
