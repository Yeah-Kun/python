from PIL import Image
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"D:\Users\Yeah_Kun\Downloads\tesseract-Win64"

img_path = 'v.BMP'
image = Image.open(img_path)
#imgry = image.convert('L')  # 转化为灰度图
# table = get_bin_table()
# out = imgry.point(table, '1')
aa = pytesseract.image_to_string(image)
print (aa)