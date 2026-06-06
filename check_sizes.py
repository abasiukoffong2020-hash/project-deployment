import os
p = r"c:\Users\ADMIN\OneDrive\Documents\ML dataset\Loan Approval"
for f in sorted(os.listdir(p)):
    path = os.path.join(p, f)
    if os.path.isfile(path):
        size = os.path.getsize(path)
        print(f"{f}\t{size}")
