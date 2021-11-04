#import required modules
from collections import deque
import paramiko 
import paramiko.client
from properties import get_Credentials 
from stat import S_ISDIR,S_ISREG
import time 
import os 


#connecting to remote linux server using ssh
def RemoteServerConnect():
    try:
        connect_strings=get_Credentials() 
        host=connect_strings['hostname'] 
        user=connect_strings['username']
        passw=connect_strings['password'] 

        ssh=paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.client.AutoAddPolicy) 
        ssh.connect(hostname=host,username=user,password=passw)
        print("Successfully Connected to ",host) 
        return ssh 

    except paramiko.AuthenticationException:
        print("Failed to connect to host due to wrong username or password!") 
        exit(1) 
    except Exception as e:
        print(e) 
        exit(2)


#execute linux commands in connected linux server
def executeCommandsConsole(ssh):
    cmd=input("Enter Command>>")
    try:
        stdin,stdout,stderr=ssh.exec_command(cmd)
    except Exception as e:
        print(e) 

    err="\n".join(stderr.readlines()) 
    out="\n".join(stdout.readlines())
    final_output=str(err)+str(out)
    print("*******************************************************************")
    print(final_output)
    print("********************************************************************")



#execute and save the output of commands executed in remote server to a local file
def executeCommandSaveLocal(ssh):
    cmd=input('Enter  Command>>')
    try:
        stdin,stdout,stderr=ssh.exec_command(cmd) 
    except Exception as e:
        print(e) 
    
    err="\n".join(stderr.readlines()) 
    out="\n".join(stdout.readlines())
    final_output=str(err)+str(out)

    t=time.localtime()
    timestamp=time.strftime("%Y%m%d_%H-%M-%S")
    file=str("log_{}.txt".format(timestamp))
    path=os.path.join(os.getcwd(),file)
    with open(path,'a+') as f:
        f.write("##########################################################################\n") 
        f.write(final_output) 
        f.write("###########################################################################\n") 
        f.write("\n")

    print("************************************************************************")
    print(final_output)
    print("************************************************************************")  



#list directories of the connected linux server w.r.t root folder
def list_directory(ssh):
    from collections import deque
    sftp=ssh.open_sftp()
    dirs=sftp.listdir()
    for i in dirs:
        print("/"+str(i))

    """
    remotedir="/home/testAdmin/django"
    dirs_to_explore=deque([remotedir])
    list_of_files=deque([])

    while len(dirs_to_explore)>0:
        try:
            current_dir=dirs_to_explore.popleft() 
            
            for entry in sftp.listdir_attr(current_dir):
                current_fileordir=current_dir+"/"+entry.filename 

                if S_ISDIR(entry.st_mode):
                    dirs_to_explore.append(current_fileordir)
                    print(current_fileordir)
                elif S_ISREG(entry.st_mode):
                    list_of_files.append(current_fileordir)
        except PermissionError:
            pass
    print(list_of_files)

    """


#main function menu driven logic
def main():
    while True:
        print("1.connect\n2.save\nquit(q\Q)")
        choice=input(">>")
        choice=choice.lower()
        if choice=="connect":
            ssh=RemoteServerConnect()
            while True:
                ch=input("<<Enter Key or 'quit' or 'listdir>>")
                ch=ch.lower() 
                if ch=='':
                    executeCommandsConsole(ssh)
                    continue 
                elif ch=='listdir':
                    list_directory(ssh)
                    continue
                elif ch=='quit':
                    ssh.close()
                    break
        elif choice=='save':
            ssh=RemoteServerConnect() 
            while True:
                ch=input("<<Enter Key or 'quit'>>")
                ch=ch.lower()
                if ch=='':
                    executeCommandSaveLocal(ssh)
                    continue 
                elif ch=='quit':
                    ssh.close()
                    break 
        elif choice=='q':
            ssh.close()
            break 


#main
if __name__=='__main__':
    main()

    



        
