## Generate markdown (.md) files for Documenting APIs stored in hopscotch

1. Download the API(s) as a collection by moving them to specific folders and Exporting to your computer (download as .json)
2. Download this python script into the same folder where you downloaded the files
3. Open the script and manually change the folder names which contain the API(s) - recall these folders were created in hopscotch to group your API(s) as collections.

Change this **list** in the following block:
```python
files = ["FILENAME.EXTENSION","Something.pdf"]
```
etc. whatever file name you have given along with the extension.
You can add as many files as you want into the list or change this block as you wish with your expertise.
![image](https://github.com/user-attachments/assets/5481b7e2-0685-42e0-9496-7dbcc93161b0)

_Note_: You don't actually need to store the API(s) as folders, you could just download a single API and run this script to create the documentation just fine. This is still a work-in-progress. This is the first version I made.

An example of how the documentation may look:
![image](https://github.com/user-attachments/assets/5a4301f0-5726-47fe-9b69-16d29d527544)
