# image_formats.py
from wagtail.images.formats import Format, register_image_format

register_image_format(
    Format('thumbnail right float', 'Thumbnail Right Float', 'richtext-image-thumbnail-right-float', 'max-500x500')
)
register_image_format(
    Format('thumbnail left float', 'Thumbnail Left Float', 'richtext-image-thumbnail-left-float', 'max-500x500')
)
register_image_format(
    Format('thumbnail right 500', 'Thumbnail Right 500', 'richtext-image-thumbnail-right', 'max-500x500')
)
register_image_format(
    Format('thumbnail left 500', 'Thumbnail Left 500', 'richtext-image-thumbnail-left', 'max-500x500')
)
register_image_format(
    Format('full width', 'Full Width', 'richtextimagefullimage', 'width-1920')
)
register_image_format(
    Format('half width right float', 'Half Width Right Float', 'richtext-image-halfwidth-right-float', 'width-800')
)
register_image_format(
    Format('half width left float', 'Half Width LeftFloat', 'richtext-image-halfwidth-left-float', 'width-800')
)
register_image_format(
    Format('half width right', 'Half Width Right', 'richtext-image-halfwidth-right', 'width-800')
)
register_image_format(
    Format('half width left', 'Half Width Left', 'richtext-image-halfwidth-left', 'width-800')
)
