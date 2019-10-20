import ipcalc
import json
import os.path

def greeting():
    try:
        #create a loop for main window
        loop=True
        while loop:
            action = input("""
    #########################################
    #                                       #  
    #  Simple IP Management Tool            #
    #  1 => Create a new subnet             #
    #  2 => Check IP database               #
    #  3 => Assign to a host name           #
    #  5 => Exit Simple IP Management Tool  #
    #                                       #
    #########################################
            
    Enter a number from 1 to 4: """)
            while action not in ["1", "2", "3", "4", "5"]:
                action = input("""
    #########################################
    #                                       #  
    #  Simple IP Management Tool            #
    #  1 => Create a new subnet             #
    #  2 => Check IP database               #
    #  3 => Assign to a host name           #
    #  5 => Exit Simple IP Management Tool  #
    #                                       #
    #########################################
        
    ##Incorrect-Choice##
    Enter a number from 1 to 4 : """)
            if action =="1":
                create()
            if action=="2":
                check()
            if action=="3":
                assign()
            if action=="4":
                print("Coming Soon")
            if action=="5":
                #exit loop when loop is false
                loop=False
    except:
        print("Error")




def create():
    range={}   #a dictionary where IPs in same subnet will be added
    i = 1      #ID number for IPs
    subnet = input("\nPlease enter the network address and mask (EX:10.10.10.0/24):")
    filename = str(subnet).replace("/","_") + ".txt"  #a filename
    for ip in ipcalc.Network(subnet):
        range[i] = [str(ip), " available for use"]  #add ips to dictionary
        i += 1                                      #id for each IP
    print(subnet, "\nSuccessfully created")
    for key, value in range.items():   #print all the created IPs in same subnet
        # print(key,"-",value.join(":"))
        print(key, "=>", ":".join(value))
    if not os.path.exists(filename):   # check and create file if not exist
        json.dump(range, open(filename, 'w'))
    if not os.path.exists("subnets.txt"):   #check and create file if not exist
        json.dump({}, open("subnets.txt", 'w'))
    add_file_name(subnet, filename)          #call     add_file_name function to add network address  and file name in   subnets.txt


def add_file_name(subnet,filename):
    d = {}
    if not os.path.exists("subnets.txt"):  #create file if not exist
        json.dump(d, open("subnets.txt", 'w'))
    subnets = json.load(open("subnets.txt"))  # load file with json to dictionary
    subnets[subnet]=filename                  # add new subnet  and file address to this file
    json.dump(subnets, open("subnets.txt", 'w'))   #write dictionary back to file with json

def assign():
    print("\nAvailable Subnets in Database\n")
    subnets = json.load(open("subnets.txt"))
    for key, value in subnets.items():   # print all the subnets
        print(key)
    network_mask = input("\nEnter the network address to see available IPs: ")
    while network_mask not in subnets.keys():  # while loop will continue asking until getting right value
        network_mask = input("\nPlease enter a correct address from listed addresses above: ")
    file_name = subnets[network_mask]  #this gives the file name for that subner
    picked_range = json.load(open(file_name))   #open selected file
    for key, value in picked_range.items():     #print IPs in selected file
        print(key, "=>", ":".join(value))
    next=True   #while loop will go on until next is false
    while next:
        key = input("\nPlease enter the IP ID to edit: ")
        while key not in picked_range.keys():
            key = input("\nIncorrect ID. Please enter the correct ID: ")
        value = input("Enter the name for {}: ".format(picked_range[key][0]))
        picked_range[key][1] = value    #change the selected key value
        json.dump(picked_range, open(file_name, 'w'))
        another = input("\nDo you want to update another IP? (enter y or n): ")
        while another not in ["y", "n", "Y", "N"]:
            another = input("\nIncorrect choice please enter y or n: ")
        if another=="y":
            next = True
        else:
            next = False

def check():
    if not os.path.exists("subnets.txt"):
        print("\nNo subnets created yet. Press 1 to add subnets")
    else:
        print("\nAvailable Subnets in Database")
        subnets = json.load(open("subnets.txt"))
        for key, value in subnets.items():
            print(key)
        network_mask = input("\nEnter the network address to see available IPs: ")
        while network_mask not in subnets.keys():
            network_mask = input("\nPlease enter a correct address from listed addresses above: ")
        file_name = open(subnets[network_mask])
        picked_range = json.load(file_name)
        for key, value in picked_range.items():
            print(key, "=>", ":".join(value))




greeting()

