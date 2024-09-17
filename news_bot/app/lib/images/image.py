import textwrap

import cv2
import numpy as np

from PIL import ImageFont, ImageDraw, Image


class ConvertImage:

    def __init__(
            self,
            title="Заголовок",
            # group_name="Название группы",
            _path_to_image="../../../src/images/vision/MacBook Pro 14_ - 1.jpg",
            _path_to_save_image="test.png",
            _path_to_font="../../../src/fonts/Gilroy-ExtraBold.ttf",
            font_size_title=42,
            # font_size_group=28
    ):
        self._title = title
        # self._group_name = group_name

        self._path_to_image = _path_to_image
        self._path_to_save_image = _path_to_save_image
        self._path_to_font = _path_to_font

        self._image = self.__get_start_image()
        self._draw = self.__get_draw()

        self._size_title = font_size_title
        # self._size_group = font_size_group

        self._font_title = self.__get_font(font_size_title)
        # self._font_group = self.__get_font(font_size_group)

    def convert_image(self):
        # position_title = ((int)(self._image.width/10), (int)(self._image.height/10))
        # position_title = ((int)(self._image.width / 2), (int)(self._image.height / 2))
        fill = (255, 255, 255, 0)
        text = textwrap.wrap(self._title, width=self._size_title)

        current_h = self._image.height / 2
        for line in text:
            w, h = self._draw.textsize(line, font=self._font_title)
            position_title = (((self._image.width - w) / 2), current_h)
            self._draw.text(
                position_title,
                line,
                # anchor="ma",
                font=self._font_title,
                fill=fill
            )

            current_h += h + 10

        # position_group = ((int)(self._image.width*7/10), (int)(self._image.height/10))
        # self._draw.text(
        #     position_group,
        #     self._group_name,
        #     font=self._font_group,
        #     fill=fill
        # )

    def __get_start_image(self):
        # image = np.load(self._path_to_image)
        # image = Image.fromarray(image)

        image = Image.open(self._path_to_image)
        data = np.asarray(image)
        image = Image.fromarray(data)

        return image

    def __get_draw(self):
        draw = ImageDraw.Draw(self._image)

        return draw

    def __get_font(self, font):
        return ImageFont.truetype(self._path_to_font, font)

    def save_image(self):
        image = cv2.cvtColor(np.array(self._image), cv2.COLOR_RGB2RGBA)
        image = Image.fromarray(image)

        image.save(self._path_to_save_image)


if __name__ == '__main__':
    image_ = ConvertImage(title="Финансовый сектор стал лидером по объему сделок M&A в начале 2023 года")
    image_.convert_image()
    image_.save_image()

