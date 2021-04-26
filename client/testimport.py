import os, sys
root = os.path.abspath(os.path.join(os.path.dirname(sys.argv[0]), ".."))
print(f"{root=}")
sys.path.append(root)

print("testing import")
import postman
