# https://github.com/miurahr/py7zr
# https://py7zr.readthedocs.io/en/stable/user_guide.html#make-archive
import py7zr
import shutil



def extract():
  archive = py7zr.SevenZipFile('sample.7z', mode='r')
  #archive.extractall(path="/tmp")
  archive.extractall('./base_dir')
  archive.close()

filenames = ['example.7z.0001', 'example.7z.0002']

output_file = 'target.7z'

def compress():
  #with py7zr.SevenZipFile('target.7z', 'w') as archive:
    #archive.writeall('./', 'base')#folder

  with py7zr.SevenZipFile(output_file, 'w') as archive:
    archive.write("./settings.prc")
    #archive.close()#nope wrong code way

  #append when there file 7z exist to append
  with py7zr.SevenZipFile(output_file, 'a') as archive:
    #archive.write("./settings.prc")
    archive.write("./requirements.txt")
    #archive.close()


if __name__ == '__main__':
  #extract()
  compress()
  print("finish...")