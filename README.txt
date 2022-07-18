# UPDATE
This was just a little file analyzer I made one night for fun. It's kinda neat, but unreliable and very hacked together. I plan to fork laika and push updates to the new repo periodically as a fun little side project.


~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Dependencies:

Install oletools:

sudo -H pip install -U oletools

Install ViperMonkey and add vmonkey to your path:

https://github.com/decalage2/ViperMonkey

If you run pip install -U -e . from the directory where setup.py is, it should automatically create entry points vmonkey and vbashell that you can run from anywhere. (no .py extension)

Make sure privileges are correct or it will have issues importing various modules.

Directory Structure:

scripts/
       output/
       carved_files/
       lazyanalyzer.py


How to run:

python3 lazyanalyzer.py --infile file

Script will use hachoir to determine what type of file it is. It will get exif data using exiftool. Then it will extract and run various tools such as olevba, oleobj, vipermonkey.

Output will be stored in the output directory. Any carved files will go into the carved_files directory.

TODO:

Check extracted IOCs in VT using VT API.
Check hashes of carved files in VT using VT API.
WGET URIs from extracted IOCs (to pull down malware, phishing page, etc)
