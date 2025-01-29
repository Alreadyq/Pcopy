import os
os.environ['TK_SILENCE_DEPRECATION']='1'
import shutil
import exifread
from datetime import datetime
from tkinter import Tk, Listbox, Button, END, filedialog, messagebox
from tqdm import tqdm

import objc
from Cocoa import NSApplication, NSWindow, NSButton, NSRect, NSPoint, NSSize, NSTableView, NSTableColumn, NSScrollView, NSApp, NSApplicationActivationPolicyRegular, NSObject, NSRunningApplication, NSApplicationActivateIgnoringOtherApps

def get_image_dates(source_folder):
    """读取 RAW/DNG/JPG 等文件的拍摄日期（优先从 EXIF 中提取 DateTimeOriginal)"""
    date_dict = {}
    # 支持常见 RAW 和 DNG 扩展名（可根据需求添加）
    raw_extensions = {'.cr2', '.nef', '.dng', '.arw', '.raf', '.orf', '.rw2'}
    for filename in os.listdir(source_folder):
        filepath = os.path.join(source_folder, filename)
        _, ext = os.path.splitext(filename)
        ext = ext.lower()  # 统一转为小写
        
        # 仅处理图片文件（包括 RAW/DNG）
        if ext not in raw_extensions and ext not in ['.jpg', '.jpeg', '.png']:
            continue
        
        try:
            with open(filepath, 'rb') as f:
                tags = exifread.process_file(f, details=False)
                # 优先读取 DateTimeOriginal，若不存在则用 DateTime
                date_tag = tags.get('EXIF DateTimeOriginal') or tags.get('Image DateTime')
                if date_tag:
                    date_str = str(date_tag).split()[0]  # 取日期部分（忽略时间）
                    date = datetime.strptime(date_str, '%Y:%m:%d').date()
                    if date not in date_dict:
                        date_dict[date] = []
                    date_dict[date].append(filepath)
        except Exception as e:
            print(f"读取 {filename} 失败: {e}")
            continue
    if not os.access(filepath, os.R_OK):
            print(f"无权限读取文件: {filepath}")
    if os.access(filepath,os.R_OK):
        print(date_dict)
        print('read is over ')

    return date_dict

def copy_images(selected_date, date_dict, target_folder):
    """复制文件到目标文件夹（按日期命名）"""
    for selected_date_signal in selected_date:

     if selected_date_signal not in date_dict:
        return False
     date_str = selected_date_signal.strftime("%Y-%m-%d")
     dest_dir = os.path.join(target_folder, date_str)
     os.makedirs(dest_dir, exist_ok=True)
     for src_path in date_dict[selected_date_signal]:
        shutil.copy2(src_path, dest_dir)
        print('processing...')
                 
     
    
    

   
    # ...（同之前的 DateSelectorGUI 类）

def select_keys(date_dict):
    print("可用的键如下：")
    for index, key in enumerate(date_dict.keys(), start=1):
        print(f"{index}. {key}")

    # 提示用户输入选择
    selection = input("请输入你要选择的键的编号，多个编号用逗号分隔（例如：1,2,3）：")

    # 处理用户输入
    selected_numbers = []
    try:
        # 将用户输入的编号字符串分割成列表
        numbers = selection.split(',')
        for num in numbers:
            num = num.strip()
            if num:
                selected_numbers.append(int(num))
    except ValueError:
        print("输入无效，请输入有效的数字编号。")
        return []

    # 获取用户选择的键
    selected_keys = []
    all_keys = list(date_dict.keys())
    for num in selected_numbers:
        if 1 <= num <= len(all_keys):
            selected_keys.append(all_keys[num - 1])
        else:
            print(f"编号 {num} 无效，已忽略。")

    return selected_keys


    

if __name__ == "__main__":
    
    source_folder = filedialog.askdirectory(title="选择源图片文件夹")
    
    if source_folder:
        date_dict = get_image_dates(source_folder)
        selected_dates=select_keys(date_dict)
       
        target_folder=filedialog.askdirectory(title="选择目标图片文件夹")
        copy_images(selected_dates,date_dict,target_folder)
        print('over,ok')
