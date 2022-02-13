import csv

lines = []

if __name__ == '__main__':
    with open("comtrade.csv", 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for item in reader:
            if reader.line_num == 1:
                continue
            relation = item[0]
            if relation == "进口":
                relation1 = "进口"
                relation2 = "出口"
            else:
                relation1 = "出口"
                relation2 = "进口"
            tail = item[1]
            head = item[3]
            lines.append([head, tail, relation1])
            tail = item[2]
            lines.append([head, tail, relation2])

    with open("neo4j.csv", "w", encoding='utf-8', newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["head", "tail", "relation"])
        for line in lines:
            if line[0]:
                writer.writerow(line)