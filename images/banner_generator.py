from PIL import Image, ImageDraw, ImageFont
from config import config
import os

CIRCLE_OFFSET = 113
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


async def generate_banner(info):
    banner = Image.open(os.path.join(BASE_DIR, config.banner))
    border = (
        Image.open(
            os.path.join(
                BASE_DIR, f"images/borders/theme-{info['border']}-border.png")
        )
        .convert("RGBA")
        .resize((600, 600), Image.LANCZOS)
    )
    level = (
        Image.open(
            os.path.join(
                BASE_DIR, f"images/borders/theme-{info['border']}-ring.png")
        )
        .convert("RGBA")
        .resize((600, 600), Image.LANCZOS)
    )
    avatar_image = Image.open(info["avatar"]).resize((325, 325), Image.LANCZOS)

    avatar = Image.new("RGBA", banner.size, (255, 255, 255, 0))
    mask = Image.new("RGBA", avatar_image.size, (255, 255, 255, 0))
    ctx = ImageDraw.Draw(mask)
    ctx.ellipse(((0, 0), (325, 325)), fill="white")
    avatar.paste(avatar_image, (banner.width // 2 -
                 avatar_image.width // 2, 147), mask)

    banner = Image.alpha_composite(banner, avatar)
    level_progress = Image.new("RGBA", banner.size, (255, 255, 255, 0))
    mask = Image.new("RGBA", level.size, (255, 255, 255, 0))
    ctx = ImageDraw.Draw(mask)
    ctx.pieslice(
        ((0, 0), (600, 600)),
        start=CIRCLE_OFFSET,
        end=(360 - (CIRCLE_OFFSET - 90) * 2) *
        info["progress"] + CIRCLE_OFFSET,
        fill="white",
    )
    level_progress.paste(
        level, (banner.width // 2 - border.width // 2, 10), mask)

    banner = Image.alpha_composite(banner, level_progress)
    banner.paste(border, (banner.width // 2 - border.width // 2, 10), border)

    txt = Image.new("RGBA", banner.size, (255, 255, 255, 0))
    font = ImageFont.truetype(
        os.path.join(BASE_DIR, "images/fonts/beaufortforlolja-regular.ttf"), 40
    )
    font_name = ImageFont.truetype(
        os.path.join(BASE_DIR, "images/fonts/beaufortforlolja-regular.ttf"), 80
    )

    ctx = ImageDraw.Draw(banner)

    ctx.text(
        (banner.width // 2 - font.getsize(str(info["level"]))[0] // 2, 462),
        str(info["level"]),
        font=font,
        fill=(255, 255, 255, 255),
    )
    ctx.text(
        (banner.width // 2 - font_name.getsize(info["username"])[0] // 2, 575),
        info["username"],
        font=font_name,
        fill=(255, 255, 255, 255),
    )

    out = Image.alpha_composite(banner, txt)
    out.save(os.path.join(BASE_DIR, "images/banner.png"))

