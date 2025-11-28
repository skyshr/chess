from utils import check_auto_input
import re

def read_file(filename):
    result = []

    try:
        with open(filename, "r", encoding="utf-8") as f:
            for line in f:
                line = re.sub(r'^\d+\.\s*', '', line)
                line = line.replace(",", "").strip()

                # 3) 공백 기준 split
                parts = line.split()
                if len(parts) != 2:
                    print("File Read Error: each line must have two moves!")
                    return []
                    
                arr = []
                for p in parts:
                    left, right = p.split("->")
                    if not check_auto_input(left, 1) or not check_auto_input(right, 2):
                        return []
                    arr.append((left, right))
                result.append(arr)
    except Exception as e:
        print(f"Error Reading File: {e}")
    return result