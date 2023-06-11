from paddleocr import PaddleOCR
ocr=PaddleOCR(use_angle_cls = True,use_gpu= False) #使用CPU预加载，不用GPU
text=ocr.ocr("o.png",cls=True)                     #打开图片文件
#打印所有文本信息
for t in text:
    print(t[1][0])