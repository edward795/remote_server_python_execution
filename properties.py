#function to get credentials for remote linux server
def get_Credentials():
    credentials=dict() 
    hostname=input('Enter the Hostname:') 
    username=input('Enter the Username:') 
    password=input('Enter the Password:') 

    credentials.update({'hostname':hostname})
    credentials.update({'username':username}) 
    credentials.update({'password':password})
    
    return credentials
