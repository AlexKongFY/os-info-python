#!/usr/bin/python3

###########################################################################################################################################################

# Student name: Alex Kong
# Student code: s3
# Unit / Class code: cfc130623
# Trainer name: Kar Wei
# Project Scope: Python OS Info

###########################################################################################################################################################

# modules for os info
import platform
import socket
import os
import subprocess
import psutil
import time
import shutil

###########################################################################################################################################################

# Create an automation to display the operating system information for Windows or Linux
# 1. Display OS version
# 2. Display private IP address, public IP address and default gateway
# 3. Display harddisk size of free and used space
# 4. Display top 5 directories and their size
# 5. Display CPU usage and refresh every 10 secs

###########################################################################################################################################################

# Goals
# able to access the os info with minimum root rights for file system
# access to root directory for top 5 directory due to minimum root rights to access

##################################################################### Checking OS Info ####################################################################

# 1. Display Windows or Linux OS version 
def display_os_version():
	os_version = platform.system() + " " + platform.release() # check system name and release version with platform module
	print(f"OS Version: {os_version}\n")


######################################################################## Window Info ######################################################################


# 2. Display private IP address, public IP address and default gateway
def display_win_ip_info(): 
	# Windows private IP address
	# socket.gethostbyname() takes in hostname of (socket.gethostname(computer name)) to obtain the corresponding private IP address. 
	private_ip = socket.gethostbyname(socket.gethostname())         
	# Windows public IP address
	# Obtain the public IP by an online website and curl bash command in subprocess module if text=True to convert output in bytes as string. Then print out the value.
	public_ip = subprocess.check_output(["curl", "-s", "ifconfig.me"], text = True)
	# Display default gateway
	# use windows command ipconfig to get default gateway and strip() any empty spaces. Then slicing last 12 characters for default gateway
	default_gateway = os.popen('ipconfig | findstr "Default Gateway"').read().strip()[-12:]   

	# Print out the Windows IP addresses
	print(f"Private IP address: {private_ip}") 
	print(f"Public IP address: {public_ip}")
	print(f"Default Gateway: {default_gateway}\n")
	
###########################################################################################################################################################

# 3. Display hard disk size of free and used space
# consider a hard disk may contain multi-partitions depending on user preferences. 
def display_win_harddisk_info() :
	partitions = psutil.disk_partitions(all=True)   # list all partitions in the hard disk
	for partition in partitions: 			# loop every partition in the hard disk
		try:
			partition_info = psutil.disk_usage(partition.device)   # device more logical in Windows for disk spaces (C drive or D drive)
	
			# convert the output in bytes to GB by 1024 power of 3 in 2 decimal places
			total_space = "{:.2f}".format(partition_info.total / (1024 ** 3))
			used_space = "{:.2f}".format(partition_info.used / (1024 ** 3))
			free_space = "{:.2f}".format(partition_info.total / (1024 ** 3))
	
			# output the device disk info 
			print(f"Partition {partition.device}: ")  # partition name
			print(f"Total space: {total_space} GB")   # total disk space
			print(f"Used space: {used_space} GB")     # used disk space
			print(f"Free space: {free_space} GB\n")     # free / unused space
		except PermissionError:                       # error occurs as it needs root rights to access the partitions 
			pass									  # Will bypass the error and continue rest of the automation on os info

###########################################################################################################################################################

# 4. Display top 5 directories and their size
def get_win_directory_size(path):                  # function to check the directory size
    total_size = 0							   # the variable accummulate the total size of the directory's files and sub-directories 
    # loop through the directory contents
    # os.walk(path) is a tuple for each directory checked
    # 3 values: dirpath for path of current directory visited, "_" placeholder to ignore sub-directories and filenames for list of files
    for dirpath, _, filenames in os.walk(path):      
        for filename in filenames:                 # nested for loop through each file in the list of files within the directory
            filepath = os.path.join(dirpath, filename)        # filepath refer the directory path of the file
            try:
                total_size += os.path.getsize(filepath)       # retrieve the file size and add to total_size variable
                
            except FileNotFoundError:
                pass          # Ignore file errors for root permission and continue with the next file
    return total_size         # output the total directory size in bytes

def get_win_top_directories(root_directory, top_count=5):        # function to check all directories within the root directory
    directory_sizes = []                     # empty to store top five directories in the root directory
    for dirpath, _, _ in os.walk(root_directory):        # loop each directory in the root directory
        total_size = get_win_directory_size(dirpath)         # calculate the size of each directory with get_directory_size function
        directory_sizes.append((dirpath, total_size))    # append to the new list with directory name and size in directory_sizes variable
    
    directory_sizes.sort(key=lambda x: x[1], reverse=True)     # sort the list is descending order in directory sizes instead of default sort method
    
    print('\nTop 5 Directories by Size:')                      # title for top five directories
    for i, (directory, size) in enumerate(directory_sizes[:top_count], start=1):   # loop only first five directories in the list of directory_sizes variable and start at 1 instead of index i at 0
        print(f'{i}. {directory} - {size / (1024 ** 3):.2f} GB\n')                 # list the directory info and convert size in bytes to GB

###########################################################################################################################################################

# 5. Display CPU usage and refresh every  10 secs

def get_win_cpu_usage():
	while True:        # while = True to continnously monitor the CPU usage
		cpu_usage = psutil.cpu_percent(interval=1, percpu=True)   # retrieve cpu usage info for 1 sec interval and psutil provides of each core info related to CPU usage
		print('\nCPU Usage:')
		for i, core_usage in enumerate(cpu_usage):                # for loop cpu_usage info of the cores with every iteration
			print(f'Core {i + 1}: {core_usage}%')				  # output each core usage in %
		time.sleep(10)                                            # refresh the info every 10 secs interval on current CPU usage
        

####################################################################### Linux Info ########################################################################

# 2. Display private IP address, public IP address and default gateway
def display_linux_ip_info():
	# Linux private IP address
	# Using subprocess to check the hostname -I bash command for private IP address
	private_ip = subprocess.check_output(["hostname", "-I"], text = True)
	# Linux public IP address
	# Obtain the public IP by an online website and curl bash command in subprocess module if text=True to convert output in bytes as string. Then print out the value.
	public_ip = subprocess.check_output(["curl", "-s", "ifconfig.me"], text = True)
	# Linux default gateway
	# use os module to open the linux bash commands to get the default gateway and read the content and strip() to remove '\n' in string
	default_gateway = os.popen("route | grep UG | awk '{print $2}'").read().strip()     
	
	# Print out the Linux IP addresses
	print(f"Private IP address: {private_ip}")
	print(f"Public IP address: {public_ip}")
	print(f"Default Gateway: {default_gateway}\n")

###########################################################################################################################################################

# 3. Display hard disk size of free and used space
# consider a hard disk may contain multi-partitions depending on user preferences. 
def display_linux_harddisk_info() :
	partitions = psutil.disk_partitions()   # list all partitions in the hard disk
	for partition in partitions: 			# loop every partition in the hard disk
		partition_info = psutil.disk_usage(partition.mountpoint)   # mountpoint provide more information than device for disk spaces
	
		# convert the output in bytes to GB by 1024 power of 3 in 2 decimal places
		total_space = "{:.2f}".format(partition_info.total / (1024 ** 3))
		used_space = "{:.2f}".format(partition_info.used / (1024 ** 3))
		free_space = "{:.2f}".format(partition_info.total / (1024 ** 3))
	
		# output the device disk info 
		print(f"Partition {partition.device}: ")  # partition name
		print(f"Total space: {total_space} GB")   # total disk space
		print(f"Used space: {used_space} GB")     # used disk space
		print(f"Free space: {free_space} GB\n")     # free / unused space

###########################################################################################################################################################

# 4. Display top 5 directories and their size
def get_linux_top_directories(root_directory, top_count=5):
	directory_sizes = []                                       # list to store the directories' names and sizes
	for dirpath, _, _ in os.walk(root_directory):              # loop only each directory in dirpath in root directory but ignore the sub-directories and files in that directory
		try:
			total_size = shutil.disk_usage(dirpath).used       # checks size of the directory in the .used attribute
			directory_sizes.append((dirpath, total_size))      # append the directory name and size to the list in directory_sizes variable
		except PermissionError:                                # error for insufficient permissions to access the directory
			pass             								   # ignore the error and continue the next directory that does not need root permissions			

	directory_sizes.sort(key=lambda x: x[1], reverse=True)     # sort the list is descending order in directory sizes instead of default sort method

	print('\nTop 5 Directories by Size:')                      # title for top five directories
	for i, (directory, size) in enumerate(directory_sizes[:top_count], start=1):      # loop only first five directories in the list of directory_sizes variable and start at 1 instead of index i at 0
		print(f'{i}. {directory} - {size / (1024 ** 3):.2f} GB\n')                    # list the directory info and convert size in bytes to GB



###########################################################################################################################################################


# 5. Display CPU usage and refresh every  10 secs

def display_linux_cpu_usage():
	while True:        # while = True to continnously monitor the CPU usage
		cpu_usage = psutil.cpu_percent(interval=1, percpu=True)   # retrieve cpu usage info for 1 sec interval and psutil provides of each core info related to CPU usage
		print('\nCPU Usage:')
		for i, core_usage in enumerate(cpu_usage):                # for loop cpu_usage info with every iteration
			print(f'Core {i + 1}: {core_usage}%')                 # output each core usage in %
		time.sleep(10)                                            # refresh the info every 10 secs interval on current CPU usage
        

############################################################### Main Function for Automation ###############################################################

def get_os_info():
	display_os_version()
	# if statement to check which os version to determine the os info
	if platform.system() == "Windows":
		display_win_ip_info()              # function for Windows private IP address, public IP address and its default gateway
		display_win_harddisk_info()        # hard disk info for Windows 
		
		# Define the root directory to start the analysis on Windows ('C:\\' for the C: drive because do not need root rights)
		get_win_top_directories("C:\\")    # function to get top 5 directories from root directory for Windows 
		get_win_cpu_usage()                # Windows CPU usage
		
	elif platform.system() == "Linux":
		display_linux_ip_info()         # function for Linux private IP address, public IP address and its default gateway
		display_linux_harddisk_info()   # hard disk info for Linux
		get_linux_top_directories("/")  # function to get top 5 directories from root directory for Linux
		display_linux_cpu_usage()       # Linux CPU usage
	else:
		print('Not supported operating system.')   # output wrong os entered.
	

get_os_info()
