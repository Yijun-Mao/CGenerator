import os
import csv
import sys
import random

def read_csv(path="res.csv"):
    with open(path, "r", encoding="utf-8") as f:
        f_csv = csv.reader(f)
        all_class = set()
        data = []
        for i, row in enumerate(f_csv):
            if i==0:
                print(row)
                continue
            
            data.append([row[1].strip().replace('\n',''), int(row[2])-1, row[4]])
            all_class.add(row[4])
    
    return data, all_class

def static(data, log_path='./static.txt'):
    class_data = {}
    for _, star, classname in data:
        if classname not in class_data:
            class_data[classname] = [0]*5
        class_data[classname][star] += 1
    fw = open(log_path, "w", encoding="utf-8")
    print("There are {} pieces of comments in total".format(len(data)))
    print( "category\t|  star 1\t|   star 2\t|   star 3\t|   star 4\t|   star 5\t|  total\t")
    fw.write("There are {} pieces of comments in total\n".format(len(data)))
    fw.write( "category\t|  star 1\t|   star 2\t|   star 3\t|   star 4\t|   star 5\t|  total\n")

    for classname, star_count in class_data.items():
        output = "{}\t|  {}\t|  {}\t|  {}\t|  {}\t|  {}\t|  {}\t".format(classname, star_count[0], star_count[1], star_count[2], star_count[3], star_count[4], sum(star_count))
        print(output)
        fw.write(output+'\n')
    
    fw.close()


def save_as_EAA(data, path):
    print(path,len(data))
    with open(path,'w', encoding="utf-8") as f:
        for item in data:
            f.write(item+'\n')

def category_merge(classname):
    transform = {"数码相机":"相机", "摄像机":"相机"}
    if classname in transform:
        return transform[classname]
    else:
        return classname

def random_split_data(data, train_rate=0.8, max_len_filter=100, min_len_filter=12, class_filter=["服务器", "数码相框", "读卡器", "扫描仪", "汽车警报", "望远镜", "航拍无人机", "桌面一体机", "镜头", "摄影灯"]):
    class_data = {}
    fw = open('./static.txt', "a", encoding="utf-8")
    for comment, _, classname in data:
        if len(comment) > max_len_filter or len(comment) < min_len_filter:
            continue
        classname = category_merge(classname)
        if classname not in class_data:
            class_data[classname] = []
        class_data[classname].append(comment)
    
    train_data = []
    valid_data = []
    test_data = []

    test_rate = (1-train_rate)/2
    fw.write("\n")
    for classname, comments in class_data.items():
        print("{} has comments {}".format(classname, len(comments)))
        
        if classname in class_filter:
            continue
        fw.write("{} has comments {}\n".format(classname, len(comments)))
        length = len(comments)
        random.shuffle(comments)
        train_data += [[comment, 0, classname] for comment in comments[0:int(length*train_rate)]]
        valid_data += [[comment, 0, classname] for comment in comments[int(length*train_rate):int(length*(1-test_rate))]]
        test_data += [[comment, 0, classname] for comment in comments[int(length*(1-test_rate)):]]
    
    fw.close()
    return train_data, valid_data, test_data


def convert_data(data, root_path):
    train_data, valid_data, test_data = random_split_data(data)
    random.shuffle(train_data)
    random.shuffle(valid_data)
    random.shuffle(test_data)

    train_src = []
    train_tgt = []

    valid_src = []
    valid_tgt = []

    test_src = []
    test_tgt = []
    for i, (comment, _, classname) in enumerate(train_data):
        train_src.append(classname)
        train_tgt.append(comment)

    for i, (comment, _, classname) in enumerate(valid_data):
        valid_src.append(classname)
        valid_tgt.append(comment)

    for i, (comment, _, classname) in enumerate(test_data):
        test_src.append(classname)
        test_tgt.append(comment)

    save_as_EAA(train_src, os.path.join(root_path, "train.src.bpe"))
    save_as_EAA(train_tgt, os.path.join(root_path, "train.tgt.bpe"))

    save_as_EAA(valid_src, os.path.join(root_path, "valid.src.bpe"))
    save_as_EAA(valid_tgt, os.path.join(root_path, "valid.tgt.bpe"))

    save_as_EAA(test_src, os.path.join(root_path, "test.src.bpe"))
    save_as_EAA(test_tgt, os.path.join(root_path, "test.tgt.bpe"))
    

    



data, all_class = read_csv()
print("The categories are :")
print(len(all_class))
static(data)

convert_data(data,"./")



