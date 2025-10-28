from gui_module import start_gui

if __name__ == "__main__":
    img_path = upload_tablet_image()
    if img_path:
        print(f"Image path: {img_path}")
