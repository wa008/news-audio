import os 
import shutil

def mkdir_path(directory_path):
    # Check if the path exists and is a directory
    if os.path.isdir(directory_path):
        try:
            # ⚠️ Be very careful with shutil.rmtree()!
            # confirm = input(f"Are you absolutely sure you want to delete '{directory_path}' and all its contents? (yes/no): ")
            # if confirm.lower() == 'yes':
            shutil.rmtree(directory_path)
            print(f"Directory '{directory_path}' and its contents removed successfully.")
            # else:
            #     print("Deletion cancelled.")
        except OSError as e:
            print(f"Error removing directory '{directory_path}': {e.strerror}")
            print("This could be due to permission issues or files being in use.")
    elif os.path.exists(directory_path):
        # Path exists but is not a directory (it's a file)
        os.remove(file_path)
        print(f"Error: '{directory_path}' exists but is a file, not a directory. `shutil.rmtree` is for directories.")
    else:
        print(f"Directory '{directory_path}' does not exist.")
    os.mkdir(directory_path)