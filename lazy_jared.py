#!/usr/bin/python3

# Pass your file as an argument 

import argparse
import os
import subprocess
import re
import datetime
import chardet

def create_file():
  filename = str(datetime.datetime.now())
  filename = "output/"+filename
  with open(filename, "w") as f:
    f.write("<!DOCTYPE html>\n")
    f.write("<html>\n")
    f.write("<link rel=\"stylesheet\" type=\"text/css\" href=\"../style.css\">\n")
    f.write("<head><h3>Lazy Jared</h3></head>\n")
    f.write("<body>\n")
  return filename

def check_file_type(filename):

  s = subprocess.check_output(["hachoir-metadata", "--type", filename])
  encoding = get_encoding(filename)
  print("File encoding: " + encoding)
  s = remove_encoding(s, encoding)
  print(s)
  return s

def olevba(filename):

  s = subprocess.check_output(["olevba", filename])
  encoding = get_encoding(filename)
  s = remove_encoding(s, encoding)
  # print(s)
  return s

def oleobj(filename):

  s = subprocess.check_output(["oleobj", "-d" "carved_files/", filename])
  encoding = get_encoding(filename)
  s = remove_encoding(s, encoding)
  # print(s)
  return s

def vmonkey(filename):
  s = subprocess.check_output(["/opt/ViperMonkey-master/vipermonkey/vmonkey.py", filename])
  encoding = get_encoding(filename)
  s = remove_encoding(s, encoding)
  return s

def exiftool(filename):
  s = subprocess.check_output(["exiftool", filename])
  encoding = get_encoding(filename)
  s = remove_encoding(s, encoding)
  return s

def strings_file(filename):
  strings_list = []
  s = subprocess.check_output(["strings", "-eL", filename])
  p = subprocess.check_output(["strings", "-eS", filename])
  d = subprocess.check_output(["strings", filename])
  strings_list = s + p + d
  return strings_list

def get_encoding(filename):
  rawdata = open(filename, 'rb').read()
  result = chardet.detect(rawdata)
  charenc = result['encoding']
  if charenc is None:
    return "None"
  else:
    return charenc

def remove_encoding(byte_data, encoding):
  if encoding == "None":
    encoding = "utf-8"
  decoded_data = byte_data.decode(encoding).strip()
  return decoded_data

def extract_urls(output_string):
  urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', output_string)
  if 'http://decalage.info/python/oletools' in urls:
    urls.remove('http://decalage.info/python/oletools')
  return urls

def unzip_file(filepath):
  s = subprocess.call(["7z", "e", filepath, "-otmp"]) 
  print("unzipped")

def check_urls(filepath):
  urls = []
  with open(filepath, 'r') as inF:
    for line in inF:
      urls += re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', line)
  # print("Check URIs:")
  # print(urls)
  return urls

def file_writer(filepath, string):
  with open(filepath, "a") as f:
    f.write(string)

def remove_tmp():
  s = subprocess.check_output(["rm", "-rf", "tmp/"])
  print ("/tmp removed")

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('--infile',
                      required=True)
  args = parser.parse_args()

  fn = args.infile
  if os.path.exists(fn):
    filepath = os.path.basename(fn)
  else:
    print("File doesn't exist. Peace dawg.")
    exit()

  # Create output file and temp str var
  output_file = create_file()
  print("OUTPUT FILE IS: " + output_file)
  # File exists, let's figure out filetype
  filetype = check_file_type(filepath)

  # Let's do some analysis
  if filetype == "Microsoft Office document":
    # Exiftool
    exifout = exiftool(filepath)
    file_writer(output_file, "<div class=\"container\">")
    file_writer(output_file, "<h4>Exiftool</h4>\n\n")
    file_writer(output_file, "<div><pre>" + str(exifout) + "</pre></div>\n\n")
    file_writer(output_file, "</div>")
    # Olevba
    output = olevba(filepath)
    file_writer(output_file, "<div class=\"container\">")
    file_writer(output_file, "<h4>olevba</h4>\n\n")
    file_writer(output_file, "<div><pre>" + output + "</pre></div>\n\n")
    file_writer(output_file, "</div>")    
    urls = extract_urls(output)
    # print("Extracted URIs: ")
    file_writer(output_file, "<div class=\"container\">")
    file_writer(output_file, "<h4> Extracted URIs: </h4>\n")
    # print(urls)
    file_writer(output_file, "<p>" + str(urls) + "</p> \n\n")
    file_writer(output_file, "</div>")
    # ViperMonkey
    vm_output = vmonkey(filepath)
    file_writer(output_file, "<div class=\"container\">")
    file_writer(output_file, "<h4>ViperMonkey Output</h4>\n\n")
    file_writer(output_file, "<div><pre>" + vm_output + "</pre></div>\n\n")
    file_writer(output_file, "</div>")
    
  elif filetype == "ZIP archive":
    # Exiftool
    exifout = exiftool(filepath)
    file_writer(output_file, "<div class=\"container\">")
    file_writer(output_file, "<h4>Exiftool</h4>\n\n")
    file_writer(output_file, "<div><pre>" + str(exifout) + "</pre></div>\n\n")
    file_writer(output_file, "</div>")
    unzip_file(filepath)    
    for fname in os.listdir('tmp'):
      if fname.find('vbaProject') != -1:
        if fname.endswith('.bin'):
          output = olevba("tmp/"+fname)
          file_writer(output_file, "<div class=\"container\">")
          file_writer(output_file, "<h4>olevba</h4>\n\n")
          file_writer(output_file, "<div><pre>" + output + "</pre></div>\n\n")
          file_writer(output_file, "</div>")
          urls = extract_urls(output)
          file_writer(output_file, "<div class=\"container\">")
          file_writer(output_file, "<h4> Extracted URIs: </h4>\n")
          # print(urls)
          file_writer(output_file, "<p>" + str(urls) + "</p> \n\n")
          file_writer(output_file, "</div>")
      # Print document.xml.rels in case something is being remote loaded
      if fname == 'document.xml.rels':
        fpath = "tmp/"+fname
        file_writer(output_file, "<div class=\"container\">")
        file_writer(output_file, "<h4>Document.xml.rels URLs: </h4>\n")
        # print(fpath)
        urls = check_urls(fpath)        
        file_writer(output_file, "<p>" + str(urls) + "</p> \n\n")
        file_writer(output_file, "</div>")
      if fname.find('oleObject') != -1:
        if fname.endswith('.bin'):
          output = oleobj("tmp/"+fname)
          file_writer(output_file, "<div class=\"container\">")
          file_writer(output_file, "<h4>oleobj (If file was carved, check carved_files)</h4>\n\n")
          file_writer(output_file, "<div><pre>" + output + "</pre></div>\n\n")
          file_writer(output_file, "</div>")
          # Strings
          ole_strings = strings_file("tmp/"+fname)
          file_writer(output_file, "<div class=\"container\">")
          file_writer(output_file, "<h4>strings on ole (to see any powershell inside, etc.)</h4>\n\n")
          file_writer(output_file, "<div><pre>" + str(ole_strings) + "</pre></div>\n\n")
          file_writer(output_file, "</div>")
    # ViperMonkey
    vm_output = vmonkey(filepath)
    file_writer(output_file, "<div class=\"container\">")
    file_writer(output_file, "<h4>ViperMonkey Output</h4>\n\n")
    file_writer(output_file, "<div><pre>" + vm_output + "</pre></div>\n\n")
    file_writer(output_file, "</div>")
  remove_tmp()
