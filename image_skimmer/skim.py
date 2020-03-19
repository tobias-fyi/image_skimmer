"""Image Skimmer \\ Skim through images and organize on the fly"""

import imghdr
from collections import Counter
import os
from pprint import pprint
import shutil
import sys

import cv2


def skim(src: str, dst: str, anno: str, exts: list = [".png", ".jpg", ".jpeg"]):
    """
    Skims through images in a directory, taking action on them as needed.
    Files with extensions not in the `exts` list will be removed automatically.

    Controls
    --------
    ESC -> Exits entire program
    d -> Image is bad; delete from filesystem (WARNING: cannot be undone).
    s -> Image is good; do nothing and move forward.
    a -> Image is good, may need manual annotation; move file to destination directory.
    m -> Image is good, but mis-classified; move file to destination directory.
    
    Parameters
    ----------
    src : str, path, or path-like
        Source directory of images to skim through.
    dst : str, path, or path-like
        Destination for good images that are not of the correct class.
    anno : str, path, or path-like
        Destination for good images that may need manual annotation.
    exts : list; optional
        List of valid file extensions / file types to keep.
        Default is `[".png", ".jpg", ".jpeg"]`.
    """
    # Create destination directories if needed
    os.makedirs(dst, exist_ok=True)
    os.makedirs(anno, exist_ok=True)

    # Move into src directory
    os.chdir(src)

    # Set up loop vars
    files = sorted(os.listdir(src))  # List to manage active files
    counter = 0
    # Use while loop to be able to go both ways along active file list
    while counter < len(files):

        # Get current filename
        file = files[counter]

        if counter % 10 == 0 and counter != 0:
            print("!!...........CONGRATS..........!!")
            print(f"You are at -> {counter} <- images!")

        # Get file extension
        file_ext = os.path.splitext(file)[-1].lower()

        try:
            # Get file type
            file_type = imghdr.what(file)
        except TypeError:  # TODO: Figure out exact error
            if os.path.isfile(file):
                confirm = input(f"\n{file} is not an image.\n-> Delete file? [Y/n]\n")
                if confirm.lower() != "n":
                    os.remove(file)  # Delete file
                    files.remove(file)  # Remove from active files list
                    # Don't increment counter, because removal shifts index
                    print("\b File deleted.")
                    continue
                else:
                    print("Exiting program...")
                    sys.exit()
            else:
                print(f"{file} is a directory.")
                counter += 1  # No change in file list, increment index
                continue

        # TODO: Clean up / merge the below and above blocks
        # Remove invalid file types
        if file_ext not in exts:
            if os.path.isfile(file):
                print(f"{file} is '{file_ext}'. Deleting...")
                os.remove(file)  # Delete file
                files.remove(file)  # Remove from active files list
                # Don't increment counter, because removal shifts index
                print("\b File deleted.")
                continue
            else:
                print(f"{file} is a directory.")
                counter += 1  # No change in file list, increment index
                continue

        else:  # File has valid extension
            try:  # Load image
                img = cv2.imread(file, cv2.IMREAD_UNCHANGED)
            except cv2.error:
                confirm = input(f"\nFailed to load {file}.\n-> Delete file? [Y/n]\n")
                if confirm.lower() != "n":
                    os.remove(file)  # Delete file
                    files.remove(file)  # Remove from active files list
                    print("Deleted.")
                    continue
                else:
                    print("Exiting program...")
                    sys.exit()

            # Create and resize the display window
            window = f"{os.path.split(src)[-1]} - {file}"
            cv2.namedWindow(window, cv2.WINDOW_NORMAL)
            cv2.resizeWindow(window, (800, 800))

            try:  # Show image
                cv2.imshow(window, img)
            except cv2.error:
                confirm = input(f"\nFailed to open {file}.\n-> Delete file? [Y/n]\n")
                if confirm.lower() != "n":
                    os.remove(file)  # Delete file from filesystem
                    files.remove(file)  # Remove from active files list
                    # Don't increment counter, because removal shifts index
                    print("Deleted.")
                    continue
                else:
                    print("Exiting program...")
                    sys.exit()

            # Wait for and take action based on keystroke
            # "0" means wait indefinitely
            k = cv2.waitKey(0) & 0xFF
            if k == 27:  # ESC key exits entire program
                cv2.destroyAllWindows()
                break
            elif k == ord("s"):  # Do nothing; open next image
                cv2.destroyAllWindows()
                counter += 1
                continue
            elif k == ord("b"):  # Do nothing; open previous image
                cv2.destroyAllWindows()
                counter -= 1
                continue
            elif k == ord("m"):  # Image is good; wrong class
                if not os.path.exists(os.path.join(dst, file)):
                    shutil.move(file, dst)
                    files.remove(file)  # Remove from active files list
                    # Don't increment counter, because removal shifts index
                    print(f"File moved to '{os.path.split(dst)[-1]}'.")
                else:
                    confirm = input("\n File exists. Delete file? [Y/n]\n")
                    if confirm.lower() != "n":
                        os.remove(file)  # Delete file from filesystem
                        files.remove(file)  # Remove from active files list
                        # Don't increment counter, because removal shifts index
                    else:
                        counter += 1
                cv2.destroyAllWindows()
                continue

            # Image is good; correct class; requires manual annotation
            # i.e. image contains multiple objects
            elif k == ord("a"):
                if not os.path.exists(os.path.join(anno, file)):
                    shutil.move(file, anno)
                    files.remove(file)  # Remove from active files list
                    # Don't increment counter, because removal shifts index
                    print(f"File moved to '{os.path.split(anno)[-1]}'.")
                else:
                    cv2.destroyAllWindows()
                    confirm = input("\n File exists. Delete file? [Y/n]\n")
                    if confirm.lower() != "n":
                        os.remove(file)  # Delete file from filesystem
                        files.remove(file)  # Remove from active files list
                        # Don't increment counter, because removal shifts index
                    else:
                        counter += 1
                cv2.destroyAllWindows()
                continue
            elif k == ord("d"):  # Image is bad; delete it altogether
                os.remove(file)  # Delete file from filesystem
                files.remove(file)  # Remove from active files list
                # Don't increment counter, because removal shifts index
                print("File deleted.")
                cv2.destroyAllWindows()
                continue


def walka(root_dir: str, exts: list = None, contains: list = None):
    """
    Walks through a directory tree and counts the leaves.
    TODO: count the different types of leaves.
    
    Parameters
    ----------
    root_dir : str, path, or path-like, optional
        Root directory, by default os.getcwd()
    exts : list, optional
        List of file extensions to count, by default None
    contains : list, optional
        Keywords to use as filter or to count, by default None
    
    Returns
    -------
    [type]
        [description]
    """
    print(os.path.split(root_dir)[-1])
    # Instantiate file extension counter
    if exts:  # Only count extensions in ext list
        ext_counter = Counter(exts)
    else:  # Count all extensions in tree
        ext_counter = Counter()
    counter = 1
    for root, dirnames, filenames in os.walk(root_dir):
        for file in filenames:
            counter += 1
            ext = os.path.splitext(file)[-1].lower()
            ext_counter[ext] += 1

    print("Total files:", counter)
    print("Extensions:")
    pprint(ext_counter.most_common())

    return counter


if __name__ == "__main__":
    # Set up necessary paths
    tpds = "/Users/Tobias/workshop/buildbox/neurecycle/trashpanda-ds"
    dl = "pre_pipeline/Bing/downloads"
    root = os.path.join(tpds, dl)

    # Trash Panda Cluster
    cluster_dir = "pizza_boxes"
    cluster = os.path.join(root, cluster_dir)

    # Good images but mislabeled
    dst_name = "mis_classified"
    dst = os.path.join(cluster, dst_name)

    # Requires manual annotation; multiple objects per image
    anno_name = "manual_annotation"
    anno = os.path.join(cluster, anno_name)

    # Move mis-labeled images to the correct directory
    # mis_dir = "medication_containers"
    # medst = os.path.join(root, mis_dir)

    # Skim the item dir
    skim(src=cluster, dst=dst, anno=anno)

    # Give the stats for that item dir
    walka(cluster)
