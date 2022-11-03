from PIL import ImageTk, Image, ImageEnhance, ImageFilter


white = (255,255,255)
black = (0,0,0)

temp_file = r"C:\WINDOWS\Temp\temp.png"


# Best for light images with white bg
def filter01(filename):
    img = Image.open(filename).convert('RGB')
    white = (255,255,255)
    black = (0,0,0)
    rgb_cut = (125,125,125)
    new_img_data = []
    for color in list(img.getdata()):
        if color > rgb_cut:
            new_img_data += [(int(int(color[0])*1.5), int(int(color[1])*1.5), int(int(color[1])*1.5))]
        elif color <= rgb_cut:
            new_img_data += [(int(int(color[0])*0.3), int(int(color[1])*0.3), int(int(color[1])*0.3))]
        else:
            new_img_data += [color]

    im2 = Image.new(img.mode, img.size)
    im2.putdata(new_img_data)
    im2.save(temp_file)
    return im2

#best for dark text editors like Atom. Best for dark backgrouds
def filter02(filename):
    img = Image.open(filename).convert('RGB')
    white = (255,255,255)
    black = (0,0,0)
    rgb_cut = (40,40,40)
    new_img_data = []
    for color in list(img.getdata()):
        if color > rgb_cut:

            new_img_data += [white]
        elif color <= rgb_cut:
            new_img_data += [black]
        else:
            new_img_data += [color]

    im2 = Image.new(img.mode, img.size)
    im2.putdata(new_img_data)
    im2.save(temp_file)
    return im2


# middle cut 145 "color[0] > middle[0] or color[1] > middle[1]...."
def filter03(filename):
    img = Image.open(filename).convert('RGB')
    white = (255,255,255)
    black = (0,0,0)
    rgb_cut = (145,100,110)
    new_img_data = []
    for color in list(img.getdata()):
        if color[0] > rgb_cut[0] or color[1] > rgb_cut[1] or color[2] > rgb_cut[2] :

            new_img_data += [white]
        elif color <= rgb_cut:
            new_img_data += [black]
        else:
            new_img_data += [color]

    im2 = Image.new(img.mode, img.size)
    im2.putdata(new_img_data)
    im2.save(temp_file)
    return im2

def filter04(filename):
    img = Image.open(filename).convert('RGB')
    rgb_cut = (220,220,220)
    white = (256,256,256)
    black = (0,0,0)

    new_img_data = []
    for color in list(img.getdata()):
        if color > rgb_cut:

            new_img_data += [white]
        elif color <= rgb_cut:
            new_img_data += [black]
        else:
            new_img_data += [color]

    im2 = Image.new(img.mode, img.size)
    im2.putdata(new_img_data)
    im2.save(temp_file)
    return im2

def filter05(filename):
    img = Image.open(filename).convert('RGB')
    rgb_cut = (100,70,100)
    white = (256,256,256)
    black = (0,0,0)

    new_img_data = []
    for color in list(img.getdata()):
        if color[0] > rgb_cut[0] or color[1] > rgb_cut[1] or color[2] > rgb_cut[2]:
            new_img_data += [black]
        elif color <= rgb_cut:
            new_img_data += [white]
        else:
            new_img_data += [color]

    im2 = Image.new(img.mode, img.size)
    im2.putdata(new_img_data)
    im2.save(temp_file)
    return im2

def filter07(filename):
    img = Image.open(filename).convert('RGB')
    rgb_cut = (70,50,70)
    white = (256,256,256)
    black = (0,0,0)

    new_img_data = []
    for color in list(img.getdata()):
        if color > rgb_cut:
            new_img_data += [(int(int(color[0])*1.5), int(int(color[1])*1.5), int(int(color[1])*1.5))]
        elif color <= rgb_cut:
            new_img_data += [(int(int(color[0])*0.3), int(int(color[1])*0.3), int(int(color[1])*0.3))]
        else:
            new_img_data += [color]

    im2 = Image.new(img.mode, img.size)
    im2.putdata(new_img_data)
    im2.save(temp_file)
    return im2

#convert to monochrom
def filter06(filename):
    img = Image.open(filename).convert('RGB')
    img_bw = img.convert("L")
    im1 = img_bw.save(temp_file)

def contrast(filename):
    print("contrast filter")
    img = Image.open(filename).convert('RGB')
    enhancer = ImageEnhance.Contrast(img)
    factor = 1.5 #increase contrast
    im_output = enhancer.enhance(factor)
    im_output.save('temp_cont.png')

def sharpen():
    img = Image.open("temp.png").convert('RGB')
    sharpened1 = img.filter(ImageFilter.SHARPEN)
    sharpened2 = sharpened1.filter(ImageFilter.SHARPEN)
    sharpened3 = sharpened2.filter(ImageFilter.SHARPEN)
    sharpened3.save(r"temp.png")
    sharpened3.show()

def smooth(filename):
    img = Image.open(filename).convert('RGB')
    smooth_img = img.filter(ImageFilter.SMOOTH)
    smooth_img.save('temp_smooth.png')
