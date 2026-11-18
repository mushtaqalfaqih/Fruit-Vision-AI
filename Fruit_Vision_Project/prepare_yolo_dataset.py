from pathlib import Path

DATASET = Path(r"C:\Users\hp\Desktop\CV\Fruit_Vision_Project\dataset_detection")
BOX_LINE = "0 0.5 0.5 1.0 1.0\n"

def fix_split(split):
    images = DATASET / "images" / split
    labels = DATASET / "labels" / split

    images_list = list(images.glob("*.*"))
    fixed = 0

    for img in images_list:
        if img.suffix.lower() not in [".jpg", ".png", ".jpeg"]:
            continue

        label = labels / (img.stem + ".txt")

        if not label.exists() or label.stat().st_size == 0:
            with open(label, "w") as f:
                f.write(BOX_LINE)
            fixed += 1

    print(f"✅ {split}: fixed {fixed} label files")

def main():
    print("🚑 FIXING VAL LABELS ...")
    fix_split("val")
    print("🎯 DONE — No empty val labels remain")

if __name__ == "__main__":
    main()
