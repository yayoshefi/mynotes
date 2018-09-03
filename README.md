# mynotes
notes and task app for linux terminal use
==========================================

I found myself working most of the day on remote linux desktop,
  to manage my task i found it inconvenient to switch to windows base task application 
Script contains the default User list in addition to any new list created
 Each list saves and shows 3 levels of importance
    (-) Task
    (-) Note
    (-) Archive
I used the script with additional alias to make it easier
also adding a simple show to crontab to show all my tasks every start of week
  
Contains:
========
mynotes.py       python script 
my_notes.json    DataBase 

How to Start:
=============
1) save the mynotes.py script and the template empty version of my_notes.json under ~/MYNOTES/
2) create a new list by running 
   $mynotes.py --new_list ListName
3) use the -h option to see all optioanl arguments (add, remove, edit, archive..)
4) when using multiple lists use the -l --list_name to specify which list to use

Recomended Alias:
=================
if (! $?MYNOTES_LIST ) then  
  setenv MYNOTES_LIST     "UserName" ; #Defalut list
endif

alias addnote            '~/mynotes.py -l $MYNOTES_LIST --add  \!*'
alias addtask            '~/mynotes.py -l $MYNOTES_LIST --addtask  \!*'
alias rmnote             '~/mynotes.py -l $MYNOTES_LIST --remove  \!* '
alias rmtask             '~/mynotes.py -l $MYNOTES_LIST --remove 100 '
alias edinote             '~/mynotes.py -l $MYNOTES_LIST --edit  \!* '
alias archnote           '~/mynotes.py -l $MYNOTES_LIST --archive  \!* '
alias notes_all          'clear ; ~/mynotes.py --show -l "*" \!* '
alias notes              '~/mynotes.py --show  -l $MYNOTES_LIST \!* '

Future Updates:
===============
1) Add notification option to a specific task- by email or directly to a tty 






