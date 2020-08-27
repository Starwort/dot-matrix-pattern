def convert(fname):
    img = pdb.gimp_file_load(fname, fname)
    print("Loaded " + fname)
    pdb.gimp_context_set_interpolation(INTERPOLATION_CUBIC)
    print("Set interpolation context")
    pdb.gimp_image_scale(img, 32, 32)
    print("Scaled image")
    pdb.gimp_image_convert_indexed(img, 0, 0, 15, False, True, "Web")
    print("Converted image to indexed palette")
    pdb.file_png_save(
        img, img.layers[0], fname + ".out.png", fname + ".out.png", 0, 9, 1, 0, 0, 1, 1
    )
    print("Exported image to " + fname + ".out.png")
    pdb.gimp_image_delete(img)
    print("Done")


# GIMP auto-execution stub
if __name__ == "__main__":
    import os, sys, subprocess

    scrdir = os.path.dirname(os.path.realpath(__file__))
    scrname = os.path.splitext(os.path.basename(__file__))[0]
    shcode = (
        "import sys;sys.path.insert(0, '"
        + scrdir
        + "');import "
        + scrname
        + ";"
        + scrname
        + ".convert"
        + str(tuple(sys.argv[1:]))
    )
    if os.pathsep == ";":
        gimp_console = "C:\\Program Files\\GIMP 2\\bin\\gimp-console-2.10.exe"
    else:
        gimp_console = "gimp-console"
    shcode = (
        ('%s -idf --batch-interpreter python-fu-eval -b "' % gimp_console)
        + shcode
        + '" -b "pdb.gimp_quit(1)"'
    )
    sys.exit(subprocess.call(shcode, shell=True))
else:
    from gimpfu import *
