# set up build for library .dll or .so for encrypt data
# cmd
# python src/setup.py build_ext --inplace
# https://www.youtube.com/watch?v=A1CqUVLda4g&list=PLKDGUSKZLg-7GwXgEPV6eN6_-JxoSheK2&index=9

'''
notes:
 Need to figure out how to handle __init__.py since override write
'''

import os
from pathlib import Path
import re
from setuptools import Extension, setup
from Cython.Build import cythonize
#import numpy

# START CONFIG
PROJECT_MODULE = "pycraft"

SRC_DIR = Path(__file__).resolve().parent
MODULE_DIR = SRC_DIR / PROJECT_MODULE
os.chdir(SRC_DIR)

#print(f"SRC_DIR: {SRC_DIR}")

try:
  extensions = []
  modules = set()

  # convert all .py files to .pyx and update __init__.py
  #with open(MODULE_DIR / "__init__.py", "w") as init_f:
  with open(MODULE_DIR / "__init__.py", "a") as init_f:
    #modules.add(f"{PROJECT_MODULE}.entrypoint\n")

    for root, dirs, files in os.walk(MODULE_DIR):
      root_path = Path(root)

      for file in files:
        #print("[[[ === dir file :", file ," ===]]]")
        if not file.endswith(".py") or file == "__init__.py":
          continue

        file_path = root_path / file

        # copy all imports into __init__.py
        # assumes black formatting
        with open(file_path, "r") as f:
          lines = f.readlines()
          
        for line in lines:
          line = line.strip()

          # contunue if import line
          if not line.startswith("import ") and not line.startswith("from "):
            continue

          # Strip comments
          # Comments can be trailing on import statements
          line = line.split("#")[0].strip()

          # Handle 'import'
          if line.startswith("import "):
            line = line.split("import")[1].strip()
            split = [mod.strip().split(" as ")[0].strip() for mod in line.split(",")]

            for mod in split:
              if mod not in modules:
                modules.add(mod)

          # Handle 'from'
          elif line.startswith("from "):
            line = line.split("from")[1].strip()
            mod = line.split("import")[0].strip()

            if mod not in modules:
              modules.add(mod)

        #rename file
        new_file_path = file_path.parent / f"{file_path.stem}.pyx"

        file_path.rename(new_file_path)
        file_path = new_file_path
        letpath = root_path / file_path.stem
        
        base_name = re.sub(
          f"^{f'{SRC_DIR.as_posix()}'}",
          "",
          (root_path / file_path.stem).as_posix(),
        )
        name = base_name.replace("/",".")
        name = name[1:]
        print("name: ", name)
        src_file = f"{base_name}.pyx"
        src_file = src_file[1:]
        sources = [src_file] #put into array
        print("sources: ", sources)
        #sources = sources[1:]
        print("sources: ", sources)
        extensions.append(Extension(name, sources))
    #extensions.append(Extension("mypackage.test", ['mypackage/test.pyx'])) # works
    setup(
      ext_modules=cythonize(
        extensions,
        annotate=False,
        compiler_directives={"language_level":"3"}
      ),
    )
  '''
  '''
finally:

  # convert all .pyx files back to py.
  for root, dir, files in os.walk(MODULE_DIR):
    root_path = Path(root)

    for file in [file for file in files if file.endswith(".pyx")]:
      file_path = root_path / file
      new_file_path = file_path.parent / f"{file_path.stem}.py"

      file_path.rename(new_file_path) # .pyx > .py
  pass