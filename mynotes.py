#!/usr/bin/python3
"""

WRITTEN BY SHEFI 15.4.18
"""
import argparse
import sys
import os
import re
import datetime
import time
import math
import json
from colorama import Fore, Back, Style
from string import Template
MYNOTES_DIR =os.environ.get('MYNOTES_DIR', os.environ.get("HOME")+'/MYNOTES')

# ====================================================================================================================
if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='printer to my notes')
    parser.add_argument('--add',             dest='add'     , action='store',    nargs='+', required=False,   default=False, help='add one or more notes to the json');
    parser.add_argument('--addtask',        dest='addtask', action='store',      nargs='+', required=False,   default=False, help='add notes to high priority list');
    parser.add_argument('--remove',          dest='remove'  , action='store',    nargs='*', required=False,   default=None , help='removes notes by thier id from the json');
    parser.add_argument('--archive',         dest='archive' , action='store',    nargs='*', required=False,   default=None , help='archives notes , notes will not be dispayed - NOT WORKINT YET');
    parser.add_argument('--edit',            dest='edit'    , action='store',    nargs=2  , required=False,   default=None , help='edits a certain note - append to end');
    parser.add_argument('-l', '--list_name', dest='list_name',action='store',    nargs='+', required=False,   default=['user'], help='set specific list name use * for all lists');
    parser.add_argument('--new_list',        dest='new_list', action='store',      required=False,   default=None , help='create new list');
    parser.add_argument('--debug',           dest='debug'   , action='store_true', required=False,   default=False, help='debug mode');
    parser.add_argument('-=', '--show',      dest='show'    , action='store_true', required=False,   default=False, help='Prints all notes');


    args = parser.parse_args()

    if (args.debug):  print ("Args list from user = {0}".format(sys.argv[1:]))
    if (args.debug):  print ("Passed arguments = {0}".format(args))
    edit = True if (args.remove != None or args.add or args.addtask or args.edit or args.archive) else  False

    notes = json.load(open(MYNOTES_DIR + '/my_notes.json','r'))

    if args.list_name == ['*'] : ls_name = list(notes.keys())
    else: ls_name = args.list_name
    if (args.debug) :print ("working on lists: (ls_name) "+str(ls_name) )


    if args.new_list:
        notes[args.new_list] = {'tasks':[],'notes':[],'edit_time':''}
        json.dump(notes,open(MYNOTES_DIR+'/my_notes.json','w'),indent=2)

# ====================================
# =========== EDIT LISTS =============
# ====================================
    time_tuple = time.localtime(time.time())
    localtime = time.asctime( time_tuple )
    short_time = time.strftime("%a %d/%m-%H:%M",time_tuple)

    ls_nm = ''
    if edit:
        if args.debug: print ("Edit mode active")
        if args.debug and len(ls_nm): print ("SHEFI ls_nm not empty")
        if args.debug and not len(ls_nm): print ("SHEFI ls_nm  empty")

        for active_list in notes.keys():
            if args.debug: print ("DEBUG: checking "+active_list)
            for list_pattern in ls_name:
                if re.search(list_pattern,active_list,re.IGNORECASE):
                    ls_nm = active_list
                    print ( " Editing  list " + active_list)

#====================================================================================================
# the edit it self
                    # =============
                    #     ADD
                    # =============
                    if args.addtask:
                        for task in args.addtask:
                            if (args.debug): print (" DEBUG: add task "+task)
                            notes[ls_nm]['tasks'].append((task,short_time))
                    if args.add:
                        for note in args.add:
                            if (args.debug): print (" DEBUG: add note "+note)
                            notes[ls_nm]['notes'].append((note,short_time))

                    # =============
                    #    REMOVE
                    # =============
                    if args.remove != None:
                        if (len(ls_name)>1) : print ("Failed - can't delete from multiple lists"); sys.exit(1)
                        if len(args.remove) == 0:           #default value when passing remove with no args is last note
                            del_note = notes[ls_nm]['notes'].pop()[0]
                            if (args.debug): print (" DEBUG: removing last note "+str(len(notes[ls_nm]['notes'])+2)+") '"+del_note+"'")
                        elif (args.remove == ['100'] ):
                            del_task = notes[ls_nm]['tasks'].pop()[0]
                            if (args.debug): print (" DEBUG: removing last task "+str(len(notes[ls_nm]['tasks'])+2)+") '"+del_task+"'")
                        else:
                            rm_ind = sorted (args.remove, key=int, reverse=True)
                            for n_id in rm_ind:
                                if int(n_id) == 100 and len(args.remove) > 1: continue  #this is the case we pass last taks and another one to remove
                                if int(n_id) < 100 : priority = 'notes';
                                else: priority = 'tasks'; n_id = int(n_id)-100;

                                del_note = notes[ls_nm][priority].pop( int(n_id)-1 )
                                if (args.debug): print (" DEBUG: removing "+priority[:-1]+" "+str(n_id)+") '"+del_note+"'")

                    if args.archive != None:
                        arc_ind = sorted (args.archive, key=int, reverse=True)
                        for n_id in arc_ind:
                            if int(n_id) == 100 and len(args.remove) > 1: continue  #this is the case we pass last taks and another one to remove
                            if int(n_id) < 100 : priority = 'notes';
                            else: priority = 'tasks'; n_id = int(n_id)-100;

                            notes[ls_nm]['archive'].append(notes[ls_nm][priority].pop( int(n_id)-1 ) )

                        pass
                    # =============
                    #     EDIT
                    # =============
                    if args.edit != None:
                        print (f"first = {args.edit[0]} typed  {type(args.edit[0])} ;  second = {args.edit[1]} typed  {type(args.edit[1])}")
                        if args.edit[0].isdigit():
                            # ("SHEFI - first arg is the note_index")
                            n_id = int(args.edit[0]);  text = args.edit[1]
                        else:
                            # ("SHEFI - second arg is the note_index")
                            n_id = int(args.edit[1]);  text = args.edit[0]
                        if n_id < 100 : priority = 'notes';
                        else: priority = 'tasks'; n_id = n_id-100;
                        notes[ls_nm][priority][n_id-1][0] += " //"+text
                        notes[ls_nm][priority][n_id-1][1] = short_time

                    # Saving json file after each changed list
                    notes[ls_nm]['edit_time'] = time.asctime( time.localtime(time.time()) )
            if ls_nm: json.dump(notes,open(MYNOTES_DIR+'/my_notes.json','w'),indent=2)
        if not ls_nm:
            print ("Error list name not found in dict"); sys.exit(1)
    elif args.debug: print ("NO EDIT")

# ====================================
# =========== Print notes ============
# ====================================

    #now = datetime.datetime.now()
    #now.strftime("%Y-%m-%d %H:%M")

    if args.show:
        tit_sylte = Fore.RED+Back.LIGHTYELLOW_EX+Style.BRIGHT
        print (f"{tit_sylte}MY NOTES   "+Fore.RESET+Fore.BLACK+localtime+Style.RESET_ALL)

        for active_list in notes.keys():
            if args.debug: print ("DEBUG: checking "+active_list)
            for list_pattern in ls_name:
                if re.search(list_pattern,active_list,re.IGNORECASE):
                    ls_nm = active_list
                    print (f"\n{tit_sylte}*{ls_nm.upper()}* last update - {Fore.RESET}{Fore.BLACK}{notes[ls_nm]['edit_time']}{Style.RESET_ALL}\n"+"="*(len(ls_nm)+41))

                    for n_id in range(len(notes[ls_nm]['tasks'])):
                        print (f"{Fore.RED}TASK {n_id+101})  {notes[ls_nm]['tasks'][n_id][1]}\t{notes[ls_nm]['tasks'][n_id][0]} {Style.RESET_ALL}")
                    sep_len = (len(notes[ls_nm]['tasks'][-1][0])+33) if notes[ls_nm]['tasks']!=[] else 0

                    #print("\033[44m"+"*"*sep_len+Style.RESET_ALL)
                    print("\033[46m"+"-"*sep_len+Style.RESET_ALL)
                    for n_id in range(len(notes[ls_nm]['notes'])):
                        print (f"NOTE {n_id+1})    {notes[ls_nm]['notes'][n_id][1]}\t{notes[ls_nm]['notes'][n_id][0]}")

                    if args.debug:
                        print("\033[46m"+"-"*sep_len+Style.RESET_ALL)
                        for n_id in range(len(notes[ls_nm]['archive'])):
                            print (f"ARCH {n_id+1})    {notes[ls_nm]['archive'][n_id][1]}\t{notes[ls_nm]['archive'][n_id][0]}")




# ====================================================================================================================

# ====================================
# ============  TRUNK   ==============
# ====================================
"""
notes template

{
  "USER": {
    "tasks": [["Go Home","Sun 03/06 17:50"]],
    "notes": [],
    "archive": [],
    "edit_time": "Sun Jun  3 17:50:44 2018"
  }
}

"""
