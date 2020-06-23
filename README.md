# kindle-tools
Collection of scripts to manipulate kindle4 collections.

### Proposed forkflow is as follows:

1. You take your Kindle with stinky mess in "documents" folder, call ```collections2filesys.py -i /media/user/Kindle/ -o ./books```  
result will be documents dir under output dir containing subdirectories for collections you have created in Kindle GUI

1. You add\delete\rename these folders, add\delete books to them. **Optionally** call ```make_filenames_readable.py -r ./books``` to, you know, make filenames readable (i.e. named by author and title).

1. Finally you call ```filesys2collections.py -r ./books```, collections.json will be created under system subdir.

1. Voila, delete everything from Kindle (backup of course would be wise solution) and put content of ./books instead. 

1. Now **reset** your Kindle. It stores collections in memory and will not re-read them until reboot.

1. Enjoy your reading.
