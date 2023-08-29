import os
from argparse import ArgumentParser
from os.path import isdir, isfile
from pathlib import Path
from zipfile import ZipFile


def main():
    parser = ArgumentParser(
        description="Create a zip file for assignment submission"
    )
    parser.add_argument("assignment", choices=[str(i+1) for i in range(5)])
    args = parser.parse_args()

    aid = args.assignment

    target_folders = [
        "aris", "config", f"reports/assignment-{aid}"
    ]
    target_files = [
        "render.py", "train.py"
    ]

    for folder in target_folders:
        print(f"Check folder {folder}... ", end="")
        if isdir(folder):
            print("OK")
        else:
            print("Not Found")
            return
    for file in target_files:
        print(f"Check file {file}... ", end="")
        if isfile(file):
            print("OK")
        else:
            print("Not Found")
            return

    out_file = Path(f"outputs/assignment-{aid}.zip")
    print(f"Creating submission file {out_file}")

    arc_prefix = f"assignment-{aid}"
    out_file.parent.mkdir(exist_ok=True)
    with ZipFile(out_file, "w") as zf:
        for folder in target_folders:
            for dirname, subdirs, files in os.walk(folder):
                if "__pycache__" in subdirs:
                    subdirs.remove("__pycache__")

                arcname = os.path.join(arc_prefix, dirname)
                print(f"Add: {arcname}")
                zf.write(dirname, arcname=arcname)
                for file in files:
                    arcname = os.path.join(arc_prefix, dirname, file)
                    print(f"Add: {arcname}")
                    zf.write(os.path.join(dirname, file), arcname)
        for file in target_files:
            arcname = os.path.join(arc_prefix, file)
            print(f"Add: {arcname}")
            zf.write(file, arcname=arcname)

    print("")
    print(f"All Done. Upload {out_file} to ELMS.")
    print("You should unzip the file and check that your report opens correctly, without any broken image links.")


if __name__ == "__main__":
    main()
