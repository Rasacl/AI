import os
from PIL import Image, ImageDraw, ImageFont



def add_text_watermark_to_folder(input_dir, output_dir,watermark_text, position, font_size = 200):
    """
    Add watermark to all images in a folder
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    for filename in os.listdir(input_dir):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')) :
            image_path = os.path.join(input_dir, filename)
            original_image = Image.open(image_path)  # 打开图片
            width, height = original_image.size
            # 创建一个新的图片，大小与原图片相同
            draw = ImageDraw.Draw(original_image)
            
            font = ImageFont.truetype("super_nought.ttf", font_size)
            
            # 获取文字的宽度和高度
            text_width = font.getmask(watermark_text).getbbox()[2]
            text_height = font.getmask(watermark_text).getbbox()[3]
            print(text_width,text_height)
            
            margin = 100
            
            a = width - text_width - margin
            b = height - text_height - margin
            
            # 应用水印
            draw.text((a,b), watermark_text, fill=(255, 255, 255, 128) ,font=font)

            # 保存图片
            output_path = os.path.join(output_dir, f'waterMarker_{filename}')
            original_image.save(output_path)
            
            
            

input_dir = "./input_dir"
output_dir = "./output_dir"
watermark_text = "Hello World"
position = (0,0)
add_text_watermark_to_folder(input_dir, output_dir, watermark_text, (50,50))