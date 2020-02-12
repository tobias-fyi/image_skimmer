"""Image Skimmer \\ Skim through images and organize on the fly"""

# Std lib
import os
from shutil import move

# Third-party
import cv2


def skim(src_dir: str, dst_dir: str, exts: list = [".png", ".jpg", ".jpeg"]):
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
    x -> Image is bad; delete from filesystem (WARNING: cannot be undone).
    
    Parameters
    ----------
    src_dir : str, path, or path-like
        Source directory of images to skim through.
    dst_dir : str, path, or path-like
        Destination for good images that are not of the correct class.
    exts : list; optional
        List of valid file extensions / file types to keep.
        Default is `[".png", ".jpg", ".jpeg"]`.
    """
    # Create destination directory if needed
    os.makedirs(dst_dir, exist_ok=True)

    # Move into src directory
    os.chdir(src_dir)

    # Set up loop vars
    files = os.listdir(src_dir)  # List to manage active files
    counter = 0
    # Use while loop to be able to move backward / forward
    while counter < len(files):
        # Extract the current file from the list
        file = files[counter]

        # Remove invalid file types
        file_ext = os.path.splitext(files[counter])[-1].lower()
        if file_ext not in exts:
            print(f"{file} is '{file_ext}'. Removing...")
            os.remove(file)  # Delete file from filesystem
            files.remove(file)  # Remove file item from list of files
            print("\b Removed.")
            counter += 1
        else:
            # Load image
            img = cv2.imread(file, cv2.IMREAD_UNCHANGED)

            # Image name
            window = f"{os.path.split(src_dir)[-1]} - {file}"

            # Create and resize window
            cv2.namedWindow(window, cv2.WINDOW_NORMAL)
            cv2.resizeWindow(window, (600, 600))

            # Show image
            cv2.imshow(window, img)

            # Wait for and take action based on keystroke
            # "0" means wait indefinitely
            k = cv2.waitKey(0) & 0xFF
            if k == 27:  # ESC key exits entire program
                cv2.destroyAllWindows()
                break
            elif k == ord("s"):  # Image is good; do nothing
                cv2.destroyAllWindows()
                counter += 1
            elif k == ord("b"):  # View previous image
                cv2.destroyAllWindows()
                counter -= 1
            elif k == ord("0"):  # Start over from beginning
                cv2.destroyAllWindows()
                counter = 0
            elif k == ord("m"):  # Image is good; wrong class
                move(file, dst_dir)
                files.remove(file)  # Remove from list
                cv2.destroyAllWindows()
                counter += 1
            elif k == ord("x"):  # Image is bad; delete it altogether
                os.remove(file)  # Delete file from filesystem
                # Remove file from list in case of backward iteration
                files.remove(file)
                cv2.destroyAllWindows()
                counter += 1


if __name__ == "__main__":
    # Set up necessary paths
    root = "/Users/Tobias/workshop/buildbox/neurecycle/trashpanda-ds/exploration/1_image_downloading/Bing/downloads"
    clusdir = "hazardous_fluid"
    dst_name = "misclasses"

    src = os.path.join(root, clusdir)
    dst = os.path.join(root, dst_name)

    skimager(src_dir=src, dst_dir=dst)
