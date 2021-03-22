## Written by: Sepehr Bazyar

from time import ctime; import hashlib #For Security Password

def Two_Digits(Number): #Namayesh 8:45 be 08:45
    if(Number < 10):
        return "0" + str(Number)
    return Number

class Bus: #Ashiya Otobus Ast
    def __init__(self, Code, Name, Origin, Destination, Hour_In, Minute_In, Hour_Out, Minute_Out, Seat):
        self.Bus_Number   = Code #Moalefe Asli Tamayoz Otobus
        self.Driver_Name  = Name
        self.Origin       = Origin
        self.Destination  = Destination
        self.Entry_Hour   = Hour_In
        self.Entry_Minute = Minute_In
        self.Exit_Hour    = Hour_Out
        self.Exit_Minute  = Minute_Out
        self.List_Seat    = ["0" for i in range(Seat)] #List Sandali("0" Sandali Khalie)

    def Reservation(self, Name, Number, Mode):
        if(Mode == "+"): #Reserve Kardan
            if(self.List_Seat[Number - 1] != "0"): print("\nThis Seat has been Occupied!")
            else: self.List_Seat[Number - 1] = Name; print("\nSuccessful Reservation!")
        else:
            if(self.List_Seat[Number - 1] != Name): print("\nThe Operation is Not Possible!") #Harki Sandali Khodesho Mitoone Cancel Kone
            else: self.List_Seat[Number - 1] = "0"; print("\nSuccessful Cancellation!")

    def Show(self):
        Void, Full = [], []
        for i in range(len(self.List_Seat)):
            if(self.List_Seat[i] == "0"): Void.append(str(i + 1))
            else: Full.append(str(i + 1) + "[" + self.List_Seat[i] + "]")
        #Namayesh List Khali be Khat Tire(-)
        if(Void == []): Void = "-"
        if(Full == []): Full = "-"
            
        print("\nThe Number of The Bus is {}".format(self.Bus_Number))
        print("Bus Driver's Name is {}".format(self.Driver_Name))
        print("Transition Route is from {} to {}".format(self.Origin, self.Destination))
        print("Arriving Time is {}:{}".format(Two_Digits(self.Entry_Hour), Two_Digits(self.Entry_Minute)))
        print("Leaving  Time is {}:{}".format(Two_Digits(self.Exit_Hour), Two_Digits(self.Exit_Minute)))
        print("List of Empty Seats are {}".format(", ".join(Void)))
        print("List of Used  Seats are {}".format(", ".join(Full)))

    def Available(self):
        H, M = list(map(int, (ctime().split(" ")[3 if(ctime().split(" ")[2] != "") else 4]).split(":")[0 : 2]))
        #Natije ctime() Masalan 'Mon Mar  1 09:44:18 2021'; Roozaye Qable 10 om Injoorie " 1" Ye Space Ezafast!
        if((self.Exit_Hour < H) or (H == self.Exit_Hour and self.Exit_Minute <= M)):  return 2 #Rafte(Ra'as Time Raftan Mire)
        elif(self.List_Seat.count("0") == 0): return 3 #Zarfiat Takmil
        elif((H < self.Entry_Hour) or (H == self.Entry_Hour and M < self.Entry_Minute)): return 1 #Nayoomade
        return 0 #Mojood to Istgah

print("Bus Reservation System Project © Sepehr Bazyar\n\nWelcome!")

Buses = {} #Dictionary Otobus
try:
    with open("Buses.txt", "r") as File:
        Lines = File.readlines()

    for i in range(0, len(Lines), 9): #Har Otobus 9 Ta Attribue(Parametr)
        Code, Array = int(Lines[i][: -1]), eval(Lines[i + 8][: -1]) #[: -1] Bara Ine Ke '\n' Ro Hesab Nakone
        Obj = Bus(Code, Lines[i + 1][: -1], Lines[i + 2][: -1], Lines[i + 3][: -1], int(Lines[i + 4][: -1]),
                    int(Lines[i + 5][: -1]), int(Lines[i + 6][: -1]), int(Lines[i + 7][: -1]), len(Array))
        Buses[Code] = Obj
        Buses[Code].List_Seat = Array
except: pass #Age File Nabashe Az Qabl Mire Akhare Barname Misaze

Users = {} #Dictionary Karbar
try:
    with open("Users.txt", "r") as File:
        Lines = File.readlines()

    for i in range(0, len(Lines), 2): #Har Karbar Ye Username Dare Ye Password
        Users[Lines[i][: -1]] = Lines[i + 1][: -1]
except: pass #Age File Nabashe Az Qabl Mire Akhare Barname Misaze

while True:
    print("""
1. Users  Log in
2. Manger Log in
3. Visit as a Guest
4. Quit
""")

    c = input("Please Enter Command Code -> ").strip(" ") #.strip(" ") Space Aval Akhar Ezafe Ro Hazf Mikone
    if(c == "1"):
        Flag = False #Parcham Moondan Dar Hesab Karbari
        Mode = input('\nDo You Have a Account?("+" For YES & "-" For NO) -> ').strip(" ")
        if(Mode == "+"):
            ID   = input("\nUsername: ")
            Pass = hashlib.sha256(input("Password: ").encode()).hexdigest() #Hash 256
            if not(ID in Users): print("\nThere Is No Account With This ID!")
            elif(Users[ID] != Pass): print("\nWrong Password!")
            else: Flag = True #Password Sahihe Vared Hesabesh Mishe
        else:
            print('\n\t"Sign Up"')
            ID   = input("\nUsername: ")
            Pass = hashlib.sha256(input("Password: ").encode()).hexdigest() #Hash 256
            if not(ID in Users):
                Users[ID] = Pass #Add to Dict
                print("\nYour Account was Created!")
                Flag = True
            else: print("\nThis Username is Already Selected")

        while Flag:
            print('''
\t"User: {}"

1. Reservation System
2. Show Reservation Information
3. List of Buses Available
4. Change Password
5. Delete Account
6. Log Out
'''.format(ID))

            c = input("Please Enter Command Code -> ").strip(" ") #.strip(" ") Space Aval Akhar Ezafe Ro Hazf Mikone
            if(c == "1"):
                Mode = input("\nSelect Reserve(+) or Cancel(-) operation -> ").strip(" ")
                Code = int(input("Bus Code = "))
                Seat = int(input("Seat Number = "))

                try:
                    if(Mode == "+" and Buses[Code].Available() < 2): Buses[Code].Reservation(ID, Seat, Mode) #Reserve Bara Por Va Rafte Nemishe(Code 2 o 3)
                    elif(Mode == "-" and Buses[Code].List_Seat[Seat - 1] != "0"): Buses[Code].Reservation(ID, Seat, Mode)
                    else: print("\nThe Operation is Not Possible!") #Ya Bara Canceli Khali Boode Ya Bara Reserve Emkan Nadashte
                except: print("\nNot Defined Bus or Seat!") #Code Otobus Qalate Ya Shomare Sandali Nist to List Sandalia

            elif(c == "2"):
                if(len(Buses) == 0): print("\nThere Is No Bus!")
                else:
                    for i in Buses:
                        Buses[i].Show()

            elif(c == "3"):
                B_0, B_1, B_2, B_3 = [], [], [], []
                for i in Buses:
                    Sit = Buses[i].Available()
                    if(Sit == 0): B_0.append(str(i)) #Mojood
                    elif(Sit == 1): B_1.append(str(i)) #Ba'dan Miad
                    elif(Sit == 2): B_2.append(str(i)) #Qablan Rafte
                    else: B_3.append(str(i)) #Zarfiatesh Por Shode
                #Age Khat Tire(-) Nazanim Hichi Chap Nemikone Jelo print()
                if(B_0 == []): B_0 = "-"
                if(B_1 == []): B_1 = "-"
                if(B_2 == []): B_2 = "-"
                if(B_3 == []): B_3 = "-"

                print("\nList of Buses at The Station: {}".format(", ".join(B_0)))
                print("List of Buses Full: {}".format(", ".join(B_3)))
                print("List of Buses not Arrived: {}".format(", ".join(B_1)))
                print("List of Buses that Left: {}".format(", ".join(B_2)))

            elif(c == "4"):
                Current = hashlib.sha256(input("\nCurrent Password = ").encode()).hexdigest() #Hash 256
                Pass = hashlib.sha256(input("New Password = ").encode()).hexdigest() #Hash 256
                if(Users[ID] == Current):
                    Users[ID] = Pass
                    print("\nSuccessful Change!")
                else: print("\nIncorrect Password!")

            elif(c == "5"):
                Pass = hashlib.sha256(input("\nEnter Password: ").encode()).hexdigest() #Hash 256
                if(Users[ID] == Pass):
                    Users.pop(ID)
                    print("\nSuccessfully Deleted!")
                    Flag = False
                else: print("\nIncorrect Password!")

            elif(c == "6"):
                print("\nGood Luck.")
                Flag = False

            else: print("\nIncorrect Input Please Try Again!") #Voroodi Qeyr Az 1 ta 6

    elif(c == "2"):
        while True:
            print('''
\t"Admin"

1. Install Bus Information
2. Show Reservation Information
3. List of Buses Available
4. Delete Bus Information
5. Exit Admin Panel
''')

            c = input("Please Enter Command Code -> ").strip(" ") #.strip(" ") Space Aval Akhar Ezafe Ro Hazf Mikone
            if(c == "1"):
                Code = int(input("\nBus Code = "))
                Name = input("Bus Driver's Name = ")
                Origin = input("Starting Point of the Bus = ")
                Destination = input("Bus Destination = ")
                Hour_In, Minute_In = list(map(int, input("Arriving Time(HH:MM) At 24:00 Form = ").split(":")))
                Hour_Out, Minute_Out = list(map(int, input("Leaving  Time(HH:MM) At 24:00 Form = ").split(":")))
                Seat = int(input("Number of Bus Seats = "))

                if not(Code in Buses): #Age Otobus Tekrari Bashe Hamoon Qabli Mimoone
                    Obj = Bus(Code, Name, Origin, Destination, Hour_In, Minute_In, Hour_Out, Minute_Out, Seat)
                    Buses[Code] = Obj
                    print("\nSuccessful Registration!")
                else: print("\nThis Bus is Repeated!")

            elif(c == "2"):
                    if(len(Buses) == 0): print("\nThere Is No Bus!")
                    else:
                        for i in Buses:
                            Buses[i].Show()

            elif(c == "3"):
                B_0, B_1, B_2, B_3 = [], [], [], []
                for i in Buses:
                    Sit = Buses[i].Available()
                    if(Sit == 0): B_0.append(str(i)) #Mojood
                    elif(Sit == 1): B_1.append(str(i)) #Ba'dan Miad
                    elif(Sit == 2): B_2.append(str(i)) #Qablan Rafte
                    else: B_3.append(str(i)) #Zarfiatesh Por Shode
                #Age Khat Tire(-) Nazanim Hichi Chap Nemikone Jelo print()
                if(B_0 == []): B_0 = "-"
                if(B_1 == []): B_1 = "-"
                if(B_2 == []): B_2 = "-"
                if(B_3 == []): B_3 = "-"

                print("\nList of Buses at The Station: {}".format(", ".join(B_0)))
                print("List of Buses Full: {}".format(", ".join(B_3)))
                print("List of Buses not Arrived: {}".format(", ".join(B_1)))
                print("List of Buses that Left: {}".format(", ".join(B_2)))

            elif(c == "4"): #Bara Taqir Mishe Pak Kard Dobare Add Kardesh
                Code = input('\nEnter Bus Code or "*" For Deleting All -> ')
                if(Code == "*"): #Hame Otobusa ro Hazf Mikone
                    Buses.clear()
                    print("\nHistory Was Cleared!")
                else:
                    try:
                        Buses.pop(int(Code))
                        print("\nBus {} Was Deleted!".format(Code)) #Shomare Otobusam Mige :)
                    except: print("\nBus {} Was Not Defined!".format(Code)) #Tarif Nashoe

            elif(c == "5"):
                print("\nGood Luck.")
                break

            else: print("\nIncorrect Input Please Try Again!") #Voroodi Qeyr Az 1 ta 5

    elif(c == "3"):
        while True:
            print('''
\t"Guest"

1. Show Reservation Information
2. List of Buses Available
3. Back
''')
            
            c = input("Please Enter Command Code -> ").strip(" ") #.strip(" ") Space Aval Akhar Ezafe Ro Hazf Mikone
            if(c == "1"):
                if(len(Buses) == 0): print("\nThere Is No Bus!")
                else:
                    for i in Buses:
                        Buses[i].Show()

            elif(c == "2"):
                B_0, B_1, B_2, B_3 = [], [], [], []
                for i in Buses:
                    Sit = Buses[i].Available()
                    if(Sit == 0): B_0.append(str(i)) #Mojood
                    elif(Sit == 1): B_1.append(str(i)) #Ba'dan Miad
                    elif(Sit == 2): B_2.append(str(i)) #Qablan Rafte
                    else: B_3.append(str(i)) #Zarfiatesh Por Shode
                #Age Khat Tire(-) Nazanim Hichi Chap Nemikone Jelo print()
                if(B_0 == []): B_0 = "-"
                if(B_1 == []): B_1 = "-"
                if(B_2 == []): B_2 = "-"
                if(B_3 == []): B_3 = "-"

                print("\nList of Buses at The Station: {}".format(", ".join(B_0)))
                print("List of Buses Full: {}".format(", ".join(B_3)))
                print("List of Buses not Arrived: {}".format(", ".join(B_1)))
                print("List of Buses that Left: {}".format(", ".join(B_2)))

            elif(c == "3"):
                print("\nGood Luck.")
                break

            else: print("\nIncorrect Input Please Try Again!") #Voroodi Qeyr Az 1 ta 3

    elif(c == "4"):
        print("\nEnd Process.")
        break #Payan Halqe
    
    else: print("\nIncorrect Input Please Try Again!") #Voroodi Qeyr Az 1 ta 4

Lines = []
for i in Buses:
    Lines.append("\n".join([str(Buses[i].Bus_Number), Buses[i].Driver_Name, Buses[i].Origin, #"\n" Har Moshakhase ro to Ye Khat Minvise
                            Buses[i].Destination, str(Buses[i].Entry_Hour), str(Buses[i].Entry_Minute),
                            str(Buses[i].Exit_Hour), str(Buses[i].Exit_Minute), str(Buses[i].List_Seat)]))
with open("Buses.txt", "w") as File:
    for i in Lines:
        File.write(i + "\n") #Etelat Otobusa To 9 Khat Poshte Ham Miad Ba'ad Belafasele Mire Otobus Ba'di

Lines = []
for i in Users:
    Lines.append("\n".join([i, Users[i]]))

with open("Users.txt", "w") as File:
    for i in Lines:
        File.write(i + "\n") #Etelat Karbara To 2 Khat Poshte Ham Miad Ba'ad Belafasele Mire Karbare Ba'di
