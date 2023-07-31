# clean up files for src to clean up cache files.
# File types for .c, .pyd, .so
import os
from pathlib import Path

# START CONFIG
PROJECT_MODULE = "pyentitycraft"

SRC_DIR = Path(__file__).resolve().parent
#print("SRC_DIR: ", SRC_DIR)
MODULE_DIR = SRC_DIR / PROJECT_MODULE
os.chdir(SRC_DIR)
#print("MODULE_DIR: ", MODULE_DIR)

# Delete all .c, .pyd and .so files in src/* folder
for root, dir, files in os.walk(MODULE_DIR):
  root_path = Path(root)

  for file in files:
    if not file.endswith(".c") and not file.endswith(".pyd") and not file.endswith(".so"):
      continue
    file_path = root_path / file
    file_path.unlink(file_path)
'''
'''