"""Image Skimmer \\ Skim through images and organize on the fly"""

# Std lib
import os
from shutil import move
from subprocess import Popen
import sys

# Third-party
import cv2


def skim(src: str, dst: str, anno: str, exts: list = [".png", ".jpg", ".jpeg"]):
    """
    Skims through images in a directory, taking action on them as needed.
    Files with extensions not in the `exts` list will be removed automatically.

    Controls
    --------
    ESC -> Exits entire program
    s -> Image is good; do nothing and move forward.
    b -> View previous image; do nothing and move backward.
    0 -> Do nothing and start over from beginning.
    m -> Image is good, but mis-classified; move file to destination directory.
    m -> Image is good, may need manual annotation; move file to destination directory.
    x -> Image is bad; delete from filesystem (WARNING: cannot be undone).
    
    Parameters
    ----------
    src : str, path, or path-like
        Source directory of images to skim through.
    dst : str, path, or path-like
        Destination for good images that are not of the correct class.
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
    files = os.listdir(src)  # List to manage active files
    # Use while loop to be able to move backward / forward
    for file in sorted(files):
        # Remove invalid file types
        file_ext = os.path.splitext(file)[-1].lower()
        if file_ext not in exts:
            print(f"{file} is '{file_ext}'. Removing...")
            os.remove(file)  # Delete file
            print("\b Removed.")
        else:
            try:  # Load image
                img = cv2.imread(file, cv2.IMREAD_UNCHANGED)
            except cv2.error as e:
                confirm = input(f"\nFailed to load {file}.\n-> Delete file? [Y/n]\n")
                if confirm.lower() != "n":
                    os.remove(file)  # Delete file
                    print("Deleted.")
                    continue
                else:
                    print("Exiting program...")
                    sys.exit()

            # Create and resize window
            window = f"{os.path.split(src)[-1]} - {file}"
            cv2.namedWindow(window, cv2.WINDOW_NORMAL)
            cv2.resizeWindow(window, (800, 800))

            try:  # Show image
                cv2.imshow(window, img)
            except cv2.error as e:
                confirm = input(f"\nFailed to show {file}.\n-> Delete file? [Y/n]\n")
                if confirm.lower() != "n":
                    os.remove(file)  # Delete file from filesystem
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
            elif k == ord("s"):  # Image is good; do nothing
                cv2.destroyAllWindows()
            elif k == ord("m"):  # Image is good; wrong class
                if not os.path.exists(os.path.join(dst, file)):
                    move(file, dst)
                    print(f"File moved to '{os.path.split(dst)[-1]}'.")
                else:
                    confirm = input("\n File exists. Delete file? [Y/n]\n")
                    if confirm.lower() != "n":
                        os.remove(file)  # Delete file from filesystem
                    continue
                cv2.destroyAllWindows()
            # Image is good; correct class; requires manual annotation
            # i.e. image contains multiple objects
            elif k == ord("a"):
                if not os.path.exists(os.path.join(anno, file)):
                    move(file, anno)
                    print(f"File moved to '{os.path.split(anno)[-1]}'.")
                else:
                    cv2.destroyAllWindows()
                    confirm = input("\n File exists. Delete file? [Y/n]\n")
                    if confirm.lower() != "n":
                        os.remove(file)  # Delete file from filesystem
                    continue
                cv2.destroyAllWindows()
            elif k == ord("d"):  # Image is bad; delete it altogether
                os.remove(file)  # Delete file from filesystem
                # Remove file from list in case of backward iteration
                cv2.destroyAllWindows()


hazardous_fluid_items = [
    "antifreeze",
    "brake_fluid",
    "engine_degreaser",
    "fungicide",
    "hazardous_fluid",
    "household_cleaners",
    "household_hazardous_waste",
    "household_hazardous_waste_products",
    "insecticide",
    "lacquer",
    "lighter_fluid",
    "manual_annotation",
    "mis_classified",
    "motor_oil",
    "transmission_fluid",
]


if __name__ == "__main__":
    # Set up necessary paths
    tpds = "/Users/Tobias/workshop/buildbox/neurecycle/trashpanda-ds"
    dl = "pre_pipeline/dl_images/Bing/downloads"
    root = os.path.join(tpds, dl)

    # Trash Panda Cluster
    cluster_dir = "hazardous_fluid"
    cluster = os.path.join(root, cluster_dir)

    # Specific item or search term
    item_dir = "motor_oil"
    src = os.path.join(cluster, item_dir)

    # Good images but mislabeled
    dst_name = "mis_classified"
    dst = os.path.join(cluster, dst_name)

    # Requires manual annotation; multiple objects per image
    anno_name = "manual_annotation"
    anno = os.path.join(cluster, anno_name)

    skim(src=src, dst=dst, anno=anno)
