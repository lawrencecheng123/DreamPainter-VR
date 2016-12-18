from PIL import Image
import subprocess
import os, glob

# image name
img_path = "target.jpg"
partition_size = 2 # DO NOT CHANGE

# command line parameters
python = "python"
filename = "evaluate.py"
ckpt = "--checkpoint"
style = "/Users/andrewyli/Documents/sketchbook/fast-style-transfer/Fast Style Transfer Models/la_muse.ckpt"
input_flag = "--in-path"
input_dir = "./input"
output_flag = "--out-path"
output_dir = "./output"

def partition_image(img_path, width_split_factor, height_split_factor):
    # write a set of images to file that are the original image cropped into sub-parts
    img = Image.open(img_path)
    box = img.getbbox()
    # for i in range(width_split_factor):
    #     for j in range(height_split_factor):
    #         img.crop((box[2] / width_split_factor * i, box[3] / height_split_factor * j, box[2] / width_split_factor * (i + 1), box[3] / height_split_factor * (j + 1))).save("./input/input" + str(i + 1) + "-" + str(j + 1) + ".jpg", format="JPEG")


    x, y = box[2] / width_split_factor, box[3] / height_split_factor

    img.crop((0, 0, x + 30, y)).save("./input/input" + str(1) + "-" + str(1) + ".jpg", format="JPEG")
    img.crop((0, y, x + 30, 2 * y)).save("./input/input" + str(1) + "-" + str(2) + ".jpg", format="JPEG")
    img.crop((x - 30, 0, 2 * x, y)).save("./input/input" + str(2) + "-" + str(1) + ".jpg", format="JPEG")
    img.crop((x - 30, y, 2 * x, 2 * y)).save("./input/input" + str(2) + "-" + str(2) + ".jpg", format="JPEG")

    return (box[2] - box[0], box[3] - box[1])


def fast_style_transfer():
    # applies fast style transfer on all the cropped images
    for f in os.listdir("./input"):
        print(f)
        subprocess.call([python, filename, ckpt, style, input_flag, input_dir + "/" + f, output_flag, output_dir + "/" + f])


def stitch(width, height, w_factor, h_factor):
    os.chdir("./output")
    out_img = Image.new("RGB", (width, height))

    i, j = 0, 0
    for f in sorted(os.listdir(".")):
        if f[5] == "t":
            continue
        sub_img = Image.open(f)
        print(f[5])
        box = sub_img.getbbox()
        if f[5] == "1":
            out_img.paste(sub_img.crop((0, 0, box[2] - 30, box[3])), (width // w_factor * j, height // h_factor * i))
        elif f[5] == "2":
            out_img.paste(sub_img.crop((30, 0, box[2], box[3])), (width // w_factor * j, height // h_factor * i))
        else:
            raise AssertionError("Rip")
        # out_img.paste(sub_img, (width // w_factor * j, height // h_factor * i))
        i += 1
        if i == w_factor:
            i = 0
            j += 1
    out_img.save("result.jpg")


def main():
    w_factor, h_factor = partition_size, partition_size
    width, height = partition_image(img_path, w_factor, h_factor)
    print("partition complete")
    fast_style_transfer()
    print("fast style transfer complete")
    stitch(width, height, w_factor, h_factor)

main()
# stitch(5120, 2560, 2, 2)
