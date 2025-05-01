import firebase_admin
from firebase_admin import credentials, db


# Initialize Firebase Admin SDK with the correct path to credentials JSON file
cred = credentials.Certificate("/mnt/data/backups/winubuntu_backup/ubuntu/Desktop/main/here/codes/infi_main/smart-home-838e8-firebase-adminsdk-pe5r7-3b1307714c.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://smart-home-838e8-default-rtdb.firebaseio.com/'
})

#write/read (except '/IOT')
db_reftem = db.reference('/IOT/tem')
db_refhum = db.reference('/IOT/hum')
db_refmoi = db.reference('/IOT/moi')
db_refiot = db.reference('/IOT')
#read 
db_refiot1 = db.reference('/IOT/A1')
db_refiot2 = db.reference('/IOT/A2')
db_refiot3 = db.reference('/IOT/A3')
db_refiot4 = db.reference('/IOT/A4')
db_refiot5 = db.reference('/IOT/A5')

def read_datamoi():
    datamoi = db_refmoi.get()
    print(datamoi)

def read_dataiot():
    dataiot = db_refiot.get()
    print(dataiot)

def read_datahum():
    datahum = db_refhum.get()
    print(datahum)

def read_datatem():
    datatem = db_reftem.get()
    print(datatem)

def read_dataiot1():
    dataiot1 = db_refiot1.get()
    print(dataiot1)

def read_dataiot2():
    dataiot2 = db_refiot2.get()
    print(dataiot2)

def read_dataiot3():
    dataiot3 = db_refiot3.get()
    print(dataiot3)

def read_dataiot4():
    dataiot4 = db_refiot4.get()
    print(dataiot4)

def read_dataiot5():
    dataiot5 = db_refiot5.get()
    print(dataiot5)



def update_a1(value):
    db_refiot.update({'A1': value})
def update_a2(value):
    db_refiot.update({'A2': value})
def update_a3(value):
    db_refiot.update({'A3': value})
def update_a4(value):
    db_refiot.update({'A4': value})
def update_a5(value):
    db_refiot.update({'A5': value})

#read_datahum()
#read_dataiot()
#read_dataiot1()
#read_dataiot2()
#read_dataiot3()
#read_dataiot4()
#read_dataiot5()
#read_datamoi()
#read_datatem()

# Example usage
# update_a1(1)
# update_a2(0)
# update_a3(1)
# update_a4(0)
# update_a5(1)    
