import os
import tkinter as tk
#import cv2
#import numpy as np
from PIL import Image, ImageTk
from tkinter import filedialog

root = tk.Tk()
result_var = tk.StringVar()
global image1
global image2
global index_right
global index_left

def open_file():
# Open the directory selection dialog
    directory_path = filedialog.askdirectory(
        parent=root, 
        initialdir="/", 
        title='Please select a directory'
        )
# Check if a directory was selected and print the path
    if directory_path:
        file_names = os.listdir(directory_path)
        path_names = [os.path.join(directory_path, name) for name in file_names]
        file_path_names="\n".join(path_names)
        file_path_names=file_path_names.replace('\\',"/")        
        full_path=file_path_names.split('\n')
        return full_path

def file_save(text2save):
    files = [('All Files', '*.*'), 
             ('Batch File', '*.bat'),
             ('Text Document', '*.txt')]
    file = filedialog.asksaveasfile(filetypes = files, defaultextension = files,mode='w')
    if file is None: # asksaveasfile return `None` if dialog closed with "cancel".
        return
    file.write(text2save)
    file.close()
    return None
    
def load_image_cv2(image_path):
    if image_path=="":
        img=Image.new("RGB", (720, 960), (255, 255, 255))
    else:
#try with PIL instead of CV2
        img=Image.open(image_path)
    
    image = img.resize((960,720),Image.Resampling.LANCZOS)

    imgtk = ImageTk.PhotoImage(image=image) 
    return imgtk

def load_left_listbox(*args):
    global index_left
    lbox1.delete(0,tk.END)
    full_path=open_file()
    for item in full_path:
        lbox1.insert(tk.END, item.strip()) # .strip() removes leading/trailing spaces
    lbox1.see(0)
    lbox1.activate(0)
    
    index_left=0
#    print (lbox1.get(0))
    image1=load_image_cv2(lbox1.get(0))
    button1.config(image=image1)
    button1.image=image1
    return None

def update_image_left(*args):
#    print(lbox1.get(tk.ACTIVE))
    global index_left
    current_selection = lbox1.curselection()
    index_left=current_selection[0]
    
    lbox1.see(tk.ACTIVE)
    image1=load_image_cv2(lbox1.get(tk.ACTIVE))
    button1.config(image=image1)
    button1.image=image1
    return None
    
def next_image_left(*args):
# Advance the right image by 1 in the right listbox
    global index_left
    current_selection = lbox1.curselection()
    if current_selection:
        # If something is selected, get the first index in the tuple
        current_index = current_selection[0]
        # Clear the current selection
        lbox1.selection_clear(current_index)
   # Calculate the next index
        next_index = current_index + 1
    else:
        next_index = index_left + 1

    index_left=next_index
 # Set the new selection
    lbox1.selection_set(next_index)
    # Also make the new selection "active" and ensure it is visible
    lbox1.activate(next_index)
    lbox1.see(next_index)
    image1=load_image_cv2(lbox1.get(next_index))
#    print (lbox1.get(next_index))
    button1.config(image=image1)
    button1.image=image1
    return None

def load_right_listbox(*args):
    global index_right
    lbox2.delete(0,tk.END)
    full_path=open_file()
    for item in full_path:
        lbox2.insert(tk.END, item.strip()) # .strip() removes leading/trailing spaces
    lbox2.see(0)
    lbox2.activate(0)
    index_right=0
    image2=load_image_cv2(lbox2.get(0))
    button2.configure(image=image2)
    button2.image=image2
    return None

def update_image_right(*args):
#    print(lbox2.get(tk.ACTIVE))
    global index_right
    current_selection = lbox2.curselection()
    index_right=current_selection[0]

    lbox2.see(tk.ACTIVE)
    image2=load_image_cv2(lbox2.get(tk.ACTIVE))
    button2.configure(image=image2)
    button2.image=image2

    return None
    
def next_image_right(*args):
# Advance the right image by 1 in the right listbox
    global index_right
    current_selection = lbox2.curselection()
    if current_selection:
        # If something is selected, get the first index in the tuple
        current_index = current_selection[0]
        # Clear the current selection
        lbox2.selection_clear(current_index)
        next_index = current_index + 1
    else:
        next_index = index_right + 1

    index_right=next_index
    # Calculate the next index
# Set the new selection
    lbox2.selection_set(next_index)
    # Also make the new selection "active" and ensure it is visible
    lbox2.activate(next_index)
    lbox2.see(next_index)
    image2=load_image_cv2(lbox2.get(next_index))
#    print (lbox2.get(next_index))
    button2.config(image=image2)
    button2.image=image2
    return None


def generate_list(*args):
#This routine will generate a script/file that will rename the Right file list with
#the offset names of the left file name box.
    list_offset=index_right - index_left
    list_left = lbox1.get(0, tk.END)
    list_right = lbox2.get(0, tk.END)
# while we can just split the two list at the offset, I think we should include all the Eagle images
    if list_offset > 0 :
        new_list_left=list_left[0:]
        new_list_right=list_right[list_offset:]
    else:
        new_list_left=list_left[list_offset:]
        new_list_right=list_right[0:]

#    new_list_left=list_left[index_left:]
#    new_list_right=list_right[index_right:]
#    list_len_left =len(new_list_left)
#    list_len_right=len(new_list_right)

#we need to do some data processing on Eagle file name--ie we only want the file name, not the path
    file_names = []
    for path in new_list_left:
        file_name = os.path.basename(path)
        file_names.append(file_name)

    combined_elements = [f"rename {item1} {item2}" for item1, item2 in zip(new_list_right, file_names)]

    final_string = "\n".join(combined_elements)
    final_string=final_string.replace('.png','.JPG')
#    print(f"{final_string}")
    file_save(final_string)		#save the file
    return None    

#Start of Main App HERE:

# Set Title as Image Loader
root.title("Visual Image Comparator")

# Set the resolution of window
root.geometry("1920x900")
# Create and grid the outer content frame
c = tk.Frame(root, pady=5, padx=5)
c.grid(column=0, row=0, sticky="news")
root.grid_columnconfigure(0, weight=0)
root.grid_rowconfigure(0,weight=0)

# Grid all the widgets
image1=load_image_cv2('')
image2=load_image_cv2('')

button1 = tk.Button(root,image=image1, borderwidth=0,command=next_image_left)
button1.grid(row=0,column=0)
button1.grid(pady=0, padx=0, sticky='nw')

button2 = tk.Button(root,image=image2, borderwidth=0, command=next_image_right)
button2.grid(row=0,column=1)
button2.grid(pady=0, padx=0, sticky='nw')
# 4. Place the button in the window

#Grid #2 layout
button3 = tk.Button(root,text= "Select Eagle Image Folder", borderwidth=5)
button3.grid(row=1,column=0)
button3.grid(pady=10, padx=10, sticky='nw')
button3.configure(command=load_left_listbox)

button4 = tk.Button(root,text="Select External Camera Image Folder", borderwidth=5)
button4.grid(row=1,column=1)
button4.grid(pady=10, padx=10, sticky='nw')
button4.configure(command=load_right_listbox)

lbox1 = tk.Listbox(root,  height=5, width=80,selectmode=tk.SINGLE)
lbox1.grid(row=1, column=0)
lbox1.grid(pady=5, padx=5)
lbox1.configure(selectmode=tk.SINGLE)

lbox2 = tk.Listbox(root,  height=5, width=80,selectmode=tk.SINGLE)
lbox2.grid(row=1, column=1)
lbox2.grid(pady=5, padx=5)
lbox2.configure(selectmode=tk.SINGLE)

lbox1.bind("<Double-Button-1>", update_image_left)
lbox2.bind("<Double-Button-1>", update_image_right)

#generate our output once the images line up
button5 = tk.Button(root,text="Generate Rename File", borderwidth=5)
button5.grid(row=2,column=0)
button5.grid(pady=10, padx=10, sticky='ne')
button5.configure(command=generate_list)

verLabel= tk.Label(root, text="Version 1.0 (c) 2026 BigCity Software")
verLabel.grid(row=2,column=0)
verLabel.grid(pady=5, padx=5, sticky='nw')


root.mainloop() # Start the GUI

