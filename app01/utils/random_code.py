# PIL
# pip install pillow
from PIL import Image, ImageDraw, ImageFont
import string
import random
from io import BytesIO


# 随机颜色
def random_color():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))


str_all = string.ascii_letters + string.digits


def random_code(size=(200, 40), length=5, point_num=200, line_num=15):
    # 生成一个 200x40的白色背景图片
    width, height = size
    img = Image.new('RGB', (width, height), color=(255, 255, 255))

    # 新建一个和图片同大小的画布
    draw = ImageDraw.Draw(img)

    # 生成字体对象
    font = ImageFont.truetype(font='static/my/font/font.ttf', size=20)

    # 书写文字,随机验证码
    valid_code = ""
    for i in range(length):
        random_char = random.choice(str_all)
        draw.text((40 * i + 20, 10), random_char, (0, 0, 0), font=font)
        valid_code += random_char
    print(valid_code)

    # 添加混淆
    # 随机生成点
    for i in range(point_num):
        x, y = random.randint(0, width), random.randint(0, height)
        draw.point((x, y), random_color())

    # 随机画线
    for i in range(line_num):
        x1, y1 = random.randint(0, width), random.randint(0, height)
        x2, y2 = random.randint(0, width), random.randint(0, height)
        draw.line((x1, y1, x2, y2), random_color())

    # 图像存储

    # 创建一个内存句柄
    f = BytesIO()

    # 将图片保存到内存句柄中
    img.save(f, "PNG")

    # 读取内存句柄
    data = f.getvalue()
    # print(data)
    return data, valid_code


if __name__ == '__main__':
    random_code()
