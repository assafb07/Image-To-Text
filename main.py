from tkinter import *
from tkinter import filedialog as fd
import os
import pytesseract
import urllib.request
from filters import *
from PIL import ImageTk, Image, ImageEnhance
import PIL.Image, PIL.ImageTk
import pytesseract
import re

bg = '#333a63' ; fg = "#fafaf0" ; button_bg = "#2b3154" ; abg = '#49555c'
afg = '#938c9e' ; fnt = 'gisha' ; fnt_size = '12' ; text_box_bg = "#333a63"
hi = '1' #buttons height;
wid = '21' #buttons width
temp_file = r"C:\WINDOWS\Temp\temp.png"
temp_file_show = r"C:\WINDOWS\Temp\temp_show.png"
temp_file_url  = r"C:\WINDOWS\Temp\url.png"
show_img_width = 350
show_img_hi = 400
show_img_bg = "#16191c"

#tesseract image to text
def image_to_text(filename, lang):
    if lang == "eng":
        custom_config = r'-l eng --psm 6'
    elif lang == "heb":
        custom_config = r'-l eng+heb --psm 6'

    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    global text01
    text01 = (pytesseract.image_to_string(filename, config=custom_config))
    print_text(text01, lang)
#    pyperclip.copy(text01)

#show text from tessaract in tkinter right frame
def print_text(text01, lang):
    new_text = ""
    counter = 0
    text_widget = Text(right_frame, width=45, height=25, font=("Helvetica", 10), wrap=WORD, relief=SUNKEN, bd = 1, fg = "white", bg = text_box_bg)

    words_list = []
    words_list = text01.split()
    text_found = text_analize(words_list)
    img_url  = url_e.get()
    if img_url != "":
        text_widget.insert("1.0", f"\n\nImage Source:\n{img_url}")
    else:
        pass
    if lang == "heb":
        tag = ['tag-right', 'right']
    elif lang == "eng":
        tag = ['tag-left', 'left']
    text_widget.tag_configure(tag[0], justify=tag[1])

    if text_found != "":
        text_widget.insert("1.0", f"\n\nEmails:\n{text_found}")
    else:
        pass

    for string in text01:
        if string == "\n":
            counter +=1
            if counter > 1:
                continue
        else:
            counter = 0
        new_text += string
    if new_text != "":
        text_widget.insert("1.0", new_text, tag[0])
    else: text_widget.insert("1.0", "Can't find text in that image")
    text_widget.bind('<Button-3>',rClicker, add='')
    text_widget.grid(row = 0, column = 0, padx = 2, pady = 2)

def text_analize(words_list):
    emails = ""
    email_list = ""
    for item in words_list:
        pattern_email = r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+"
        emails = re.match(pattern_email, item)

        if emails != None and emails.group(0) not in email_list:
            email_list += emails.group(0) + "\n"
        else:
            continue
    return email_list

def select_file():
    url_e.delete(0,END)
    global filename
    try:
        filename = fd.askopenfilename()
        showImage(filename)
        img = PIL.Image.open(filename)
        img.save(temp_file)
        return filename
    except:
        lang = "eng"
        text01 = "No file selected"
        print_text(text01, lang)

def clear_frame():
    for widgets in left_frame.winfo_children():
        widgets.destroy()

def showImage(filename):
    clear_frame()
    image_resize(filename)
    img = ImageTk.PhotoImage(PIL.Image.open(temp_file_show))
    label = Label(left_frame, image = img, width=show_img_width, height=show_img_hi, bg=show_img_bg)
    label.image = img
    label.grid(row = 0, column = 0)

def image_url():
    global filename
    img_url  = url_e.get()
    try:
        with urllib.request.urlopen(img_url) as url:
            with open(temp_file_url, 'wb') as f:
                f.write(url.read())
    except:
        pass

    try:
        img = PIL.Image.open(temp_file_url)
        img.save(temp_file)
        filename = temp_file_url
        showImage(filename)
    except:
        lang = "eng"
        text01 = "Not an Image"
        print_text(text01, lang)


def image_resize(filename):
    basewidth = 330
    img = PIL.Image.open(filename)
    if img.mode != 'RGB':
        img = img.convert('RGB')
    wpercent = (basewidth / float(img.size[0]))
    hsize = int((float(img.size[1]) * float(wpercent)))
    img = img.resize((basewidth, hsize), resample=Image.Resampling.BICUBIC)
    img.save(temp_file_show)

def save_filtered_img():
    im = Image.open(temp_file)
    save_filtered_img = fd.asksaveasfile(initialfile = "picture", mode = "w", defaultextension=".png", filetypes=(("PNG file", "*.png"),("All Files", "*.*")))
    if im.mode != "RGBA":
        im = im.convert("RGBA")
    txt = Image.new('RGBA', im.size, (255,255,255,0))

    if save_filtered_img:
        abs_path = os.path.abspath(save_filtered_img.name)
        out = Image.alpha_composite(im, txt)
        out.save(abs_path)

def on_closing():
    try:
        os.remove(temp_file)
        os.remove(temp_file_show)
        os.remove(temp_file_url)
        root.destroy()

    except:
        root.destroy()

def filters_choice(filter_num):
    match filter_num:
        case 1:
            filter01(filename)
            showImage(temp_file)
    match filter_num:
        case 2:
            filter07(filename)
            showImage(temp_file)
    match filter_num:
        case 3:
            filter03(filename)
            showImage(temp_file)
    match filter_num:
        case 4:
            filter04(filename)
            showImage(temp_file)
    match filter_num:
        case 5:
            filter05(filename)
            showImage(temp_file)
    match filter_num:
        case 6:
            filter06(filename)
            showImage(temp_file)

    match filter_num:#original image
        case 100:
            img = Image.open(filename)
            img.save(temp_file)
            showImage(filename)

def onclick(event):
    image_url()

def rClicker(e):
    ''' right click context menu for all Tk Entry and Text widgets
    '''

    try:
        def rClick_Copy(e, apnd=0):
            e.widget.event_generate('<Control-c>')

        def rClick_Cut(e):
            e.widget.event_generate('<Control-x>')

        def rClick_Paste(e):
            e.widget.event_generate('<Control-v>')
        def rClick_Select_all(e):
            e.widget.event_generate('<Control-a>')

        e.widget.focus()

        nclst=[
               (' Cut', lambda e=e: rClick_Cut(e)),
               (' Copy', lambda e=e: rClick_Copy(e)),
               (' Paste', lambda e=e: rClick_Paste(e)),
               (' Select All', lambda e=e: rClick_Select_all(e))
               ]

        rmenu = Menu(None, tearoff=0, takefocus=0)

        for (txt, cmd) in nclst:
            rmenu.add_command(label=txt, command=cmd)

        rmenu.tk_popup(e.x_root+40, e.y_root+10,entry="0")

    except TclError:
        print (' - rClick menu, something wrong')
        pass

    return "break"


def rClickbinder(r):

    try:
        for b in [ 'Text', 'Entry', 'Listbox', 'Label']: #
            r.bind_class(b, sequence='<Button-3>',
                         func=rClicker, add='')
    except TclError:
        print (' - rClickbinder, something wrong')
        pass


#right click menu for text box - copy, select all
def showMenu(event):
    global clickedWidget
    clickedWidget = event.widget
    popup.post(event.x_root, event.y_root)



filename = "text03.png"
image_resize(filename)
img = Image.open(filename).convert('RGB')
ready_to_text = temp_file
img.save(temp_file)

root = Tk()
root.configure(bg=bg)
root.title("Image To Text (Beta)")
root.maxsize(800, 500)
root.resizable(False, False)

side_frame = Frame(root)
side_frame.grid(row = 0, column = 0, rowspan = 10, sticky="nsew")
side_frame.configure(bg = bg)

top_frame = Frame(root)
top_frame.grid(row = 2, column = 0, columnspan = 4)
top_frame.configure(bg = bg)


mani_frame = Frame(root)
mani_frame.configure(bg = bg)
mani_frame.grid(row = 1, column = 0, columnspan = 4)


left_frame = Frame(root, bg="black")
left_frame.grid(row = 0, column = 1, padx = "3", pady = "3")

right_frame = Frame(root)
right_frame.grid(row = 0, column = 2, padx = "3", pady = "3")

text_widget = Text(right_frame, width=45, height=25, font=("Helvetica", 10), wrap=WORD, relief=SUNKEN, bg = text_box_bg)
#add right click mouse "copy" selected
text_widget.bind('<Button-3>',rClicker, add='')
text_widget.grid(row = 0, column = 0, padx = 2, pady = 2)

img = ImageTk.PhotoImage(PIL.Image.open(temp_file_show))
label = Label(left_frame, image = img,  width=show_img_width, height=show_img_hi, bg=show_img_bg)
label.image = img
label.grid(row = 0, column = 1, padx = "3", pady = "3")

open_button = Button(top_frame,text='Open Image', font=(fnt,fnt_size), fg=fg, bg=button_bg, activebackground = abg,
activeforeground = afg, width = wid, command=select_file)
open_button.grid(row = 1, column = 0, padx = "3", pady = "5")

eng_button = Button(top_frame, text='Image to Text',font=(fnt,fnt_size), fg=fg, bg=button_bg, activebackground = abg,
activeforeground = afg, width = wid, command=lambda:image_to_text(ready_to_text, "eng"))
eng_button.grid(row = 1, column = 1, padx = "3", pady = "5")

heb_button = Button(top_frame, text='Image to Hebrew',font=(fnt,fnt_size), fg=fg, bg=button_bg, activebackground = abg,
activeforeground = afg, width = wid, command=lambda:image_to_text(ready_to_text, "heb"))
heb_button.grid(row = 1, column = 2, padx = "3", pady = "5")

original = Button(side_frame, text='Original',font=(fnt,fnt_size), fg=fg, bg=button_bg, activebackground = abg,
activeforeground = afg, width = "10", command=lambda:filters_choice(100))
original.grid(padx = "3", pady = "5")

filter1 = Button(side_frame, text='Filter 1',font=(fnt,fnt_size), fg=fg, bg=button_bg, activebackground = abg,
activeforeground = afg, width = "10", command=lambda:filters_choice(1))
filter1.grid(padx = "3", pady = "5")

filter2 = Button(side_frame, text='Filter 2',font=(fnt,fnt_size), fg=fg, bg=button_bg, activebackground = abg,
activeforeground = afg, width = "10", command=lambda:filters_choice(2))
filter2.grid(padx = "3", pady = "5")

filter3 = Button(side_frame, text='Filter 3',font=(fnt,fnt_size), fg=fg, bg=button_bg, activebackground = abg,
activeforeground = afg, width = "10", command=lambda:filters_choice(3))
filter3.grid(padx = "3", pady = "5")

filter4 = Button(side_frame, text='Filter 4',font=(fnt,fnt_size), fg=fg, bg=button_bg, activebackground = abg,
activeforeground = afg, width = "10", command=lambda:filters_choice(4))
filter4.grid(padx = "3", pady = "5")

filter5 = Button(side_frame, text='Filter 5',font=(fnt,fnt_size), fg=fg, bg=button_bg, activebackground = abg,
activeforeground = afg, width = "10", command=lambda:filters_choice(5))
filter5.grid(padx = "3", pady = "5")

filter6 = Button(side_frame, text='Filter 6',font=(fnt,fnt_size), fg=fg, bg=button_bg, activebackground = abg,
activeforeground = afg, width = "10", command=lambda:filters_choice(6))
filter6.grid(padx = "3", pady = "5")

filter6 = Button(side_frame, text='Save Image',font=(fnt,fnt_size), fg=fg, bg=button_bg, activebackground = abg,
activeforeground = afg, width = "10", command=lambda:save_filtered_img())
filter6.grid(padx = "3", pady = "5")


url_l= Label(mani_frame, text = "Enter Image URL",  font=(fnt,fnt_size), fg=fg, bg=button_bg)
url_l.grid(row = 0, column = 2,  padx = "3", pady = "5")

url_e = Entry(mani_frame, width = "25",  font=(fnt,fnt_size), fg=fg, bg=button_bg)
url_e.bind('<Return>', onclick)
url_e.bind('<Button-3>',rClicker, add='')
url_e.grid(row = 0, column = 4,  padx = "3", pady = "5")

url_b = Button(mani_frame, width = "10", text = "get image", font=(fnt,fnt_size), fg=fg, bg=button_bg, activebackground = abg,
activeforeground = afg, command=lambda: image_url())
url_b.grid(row = 0, column = 5,  padx = "3", pady = "5")

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
