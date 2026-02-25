from datetime import datetime
from pathlib import Path

import click
from PIL import Image


SUPPORTED_FORMATS = {".png", ".jpg", ".jpeg"}


def format_kb(size_bytes: int) -> str:
    size_kb = size_bytes / 1024
    return f"{size_kb:.0f}KB"


def process_image(image: Image.Image, target_width: int, target_height: int) -> Image.Image:
    # If target is larger than input in either dimension, we need to pad
    if target_width > image.width or target_height > image.height:
        # Create new white background image
        new_image = Image.new("RGB", (target_width, target_height), (255, 255, 255))
        
        # Calculate position to center the original image
        left = (target_width - image.width) // 2
        top = (target_height - image.height) // 2
        
        # Paste original image onto white background
        new_image.paste(image, (left, top))
        return new_image
    
    # Otherwise, perform the center crop as before
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


def build_default_output(input_path: Path, target_width: int, target_height: int, timestamp: str) -> Path:
    filename = (
        f"output_{input_path.stem}_{target_width}x{target_height}_{timestamp}"
        f"{input_path.suffix.lower()}"
    )
    return Path("output") / filename


@click.command()
@click.argument(
    "input_paths",
    nargs=-1,
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
)
@click.option("--target", "target", required=True, callback=lambda _, __, value: parse_target(value))
@click.option("--output", "output_path", type=click.Path(dir_okay=False, path_type=Path))
def clip_resize(input_paths: tuple[Path, ...], target: tuple[int, int], output_path: Path | None) -> None:
    """Resize by clipping equally from each side to center the composition."""
    if not input_paths:
        raise click.ClickException("At least one input image is required.")

    target_width, target_height = target
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    failures: list[str] = []

    if output_path is not None and len(input_paths) > 1:
        raise click.ClickException("--output can only be used with a single input image.")

    for input_path in input_paths:
        if input_path.suffix.lower() not in SUPPORTED_FORMATS:
            failures.append(f"{input_path}: input format must be PNG, JPG, or JPEG.")
            continue

        final_output_path = output_path or build_default_output(
            input_path, target_width, target_height, timestamp
        )

        if final_output_path.suffix.lower() not in SUPPORTED_FORMATS:
            failures.append(f"{input_path}: output format must be PNG, JPG, or JPEG.")
            continue

        try:
            with Image.open(input_path) as image:
                processed = process_image(image, target_width, target_height)
                final_output_path.parent.mkdir(parents=True, exist_ok=True)
                processed.save(final_output_path)
        except Exception as exc:
            failures.append(f"{input_path}: {exc}")
            continue

        arrow = click.style("→", fg="yellow")
        success_message = f"✓ Processed {input_path.name} {arrow} {final_output_path.name}"
        click.echo(click.style(success_message, fg="green", bold=True))

    if failures:
        click.echo(click.style("Errors:", fg="red", bold=True))
        for failure in failures:
            click.echo(click.style(failure, fg="red"))
        raise SystemExit(1)


if __name__ == "__main__":
    clip_resize()
