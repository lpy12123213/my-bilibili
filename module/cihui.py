import os
os.chdir(".\\module")
with open("词典.txt", encoding="utf-8") as f:
    h = f.read()
    ch = list(set(h.replace("\n", "").split(", ")))
    print(f"一共搜集到{len(ch)}个字词")
os.chdir("..\\")