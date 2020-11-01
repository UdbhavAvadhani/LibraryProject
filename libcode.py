#!/Library/Frameworks/Python.framework/Versions/3.8/bin/python3
import pdb
import csv
import pickle

class address:
    def __init__(self):
        print('The next four prompts are for the library address: ')
        number       = input('Enter number: ')
        street       = input('Enter street name: ')
        city         = input('Enter city name: ')
        zipcode      = input('Enter zipcode: ')
        self.address = [number, street, city, zipcode]

class books:
    def __init__(self):
        self.masterbookdict      = {}  #all books in system
        self.bookdict            = {}  #currently available books
        self.memberdict          = {}
        self.staffdict           = {}
        self.checkedoutbooksdict = {}
    
    def printlib(self):
        for k,v in self.bookdict.items():
            print(k,v)
        
    def loadbooks(self, filename):
        columnnames = []
        with open(filename) as csv_file:
            csv_reader = csv.reader(csv_file)
            linecount = 0
            for row in csv_reader:
                if linecount == 0:
                    columnnnames = row
                if linecount > 0:
                    attributelist = row
                    self.bookdict[attributelist[1]] = attributelist[2:12]
                linecount += 1
    
    def inputbook(self, bookname, staffname):
        if self.staffdict:
            if staffname in self.staffdict.keys():
                print('The next four lines are pertaining to the new book being added: ')
                authors = input('Enter authors: ')
                isbn    = input('Enter isbn: ')
                libcode = input('Enter libcode: ')
                price   = input('Enter price: ')
                self.masterbookdict[bookname] = [author, isbn, libcode, price]
                self.bookdict[bookname] = self.masterbookdict[bookname]

    def getbookinfo(self, bookname):
        if self.masterbookdict:
            if bookname in self.masterbookdict.keys():
                print('Author: ' + self.masterbookdict[bookname][0])
                print('ISBN: ' + self.masterbookdict[bookname][1])
                print('Libcode: ' + self.masterbookdict[bookname][2])
                print('Price: ' + self.masterbookdict[bookname][3])

class member(books):
    def __init__(self):
        books.__init__(self)

    def checkoutbook(self, bookname, username):
        if self.masterbookdict:
            if self.memberdict:
                if username in self.memberdict.keys():
                    if bookname in self.bookdict.keys():
                        self.memberdict[username][1] += 1
                        self.memberdict[username][2].append(bookname)
                        self.checkedoutbooksdict[bookname] = self.bookdict[
                            bookname]
                        del self.bookdict[bookname]
                        print(bookname + ' has been successfully checked out to ' + username + '.')
                    else:
                        if bookname in self.checkedoutbooksdict.keys():
                            print(
                            'This book has already been checked out to another user.'
                            )
                        else:
                            print('This book was not found in the library.')
                else:
                    print('You are not a member, so you cannot checkout a book.')
            else:
                print('There are no members in the library yet.')
        else:
            print('No books have been added to the library yet.')

    def returnbook(self, bookname, username):
        if self.masterbookdict:
            if self.memberdict:
                if username in self.memberdict.keys():
                    if bookname in self.checkedoutbooksdict.keys():
                        if bookname in self.memberdict[username][2]:
                            self.bookdict[bookname] = self.checkedoutbooksdict[
                                bookname]
                            del self.checkedoutbooksdict[bookname]
                            del self.memberdict[username][2][
                                self.memberdict[username][2].index(bookname)]
                            self.memberdict[username][1] -= 1
                            print(bookname + ' has been succesfully returned by ' + username + '.')
                        else:
                            print('You were not the user who checked out this book.')
                    else:
                        print('This book has not been checked out.')
                else:
                    print('You are not a member, so you cannot return a book.')
            else:
                print('There are no members in the library yet.')
        else:
            print('No books have been added to the library yet.')


class staff(member):
    def __init__(self):
        member.__init__(self)

    def addmember(self, newmember, libstaff = None):
        if self.staffdict:  #Do this only when the dictionary is not empty
            if libstaff in self.staffdict.keys():
                dob = input('Enter date of birth of the new member: ')
                bookscheckedout      = 0
                bookscheckedoutnames = []
                finesdue             = 0
                self.memberdict[newmember] = [
                    dob, bookscheckedout, bookscheckedoutnames, finesdue
                ]
                print('Congratulations. ' + newmember + ' is a new member.')
            else:
                print('You are not authorized to add a new member.')
        else:
            dob = input('Enter date of birth of the head librarian: ')
            bookscheckedout      = 0
            bookscheckedoutnames = []
            finesdue             = 0
            self.memberdict[newmember] = [
                dob, bookscheckedout, bookscheckedoutnames, finesdue
            ]
    
    def removemember(self, membername, libstaff):
        if self.staffdict:
            if membername in self.memberdict.keys():
                if libstaff in self.staffdict.keys():
                    if membername not in self.staffdict.keys():
                        del self.memberdict[membername]
                        print(membername + ' has been successfully removed as a member.')
                    else:
                        print('This is a staff member. Please use the relevant method instead.')
                else:
                    print('You are not a staff member, so you cannot delete members.')
            else:
                print('This person is not a member.')
        else:
            print('There are no members to remove.')

    def addstaff(self, newstaff, otherlibstaff = None):
        if self.staffdict:
            if otherlibstaff in self.staffdict.keys():
                self.addmember(newmember=newstaff, libstaff=otherlibstaff)
                self.staffdict[newstaff] = self.memberdict[newstaff]
                print('Congratulations. ' + newstaff +
                      ' is a new staff member.')
            else:
                print('You are not authorized to add staff members.')
        else:
            self.addmember(newstaff)
            self.staffdict[newstaff] = self.memberdict[newstaff]
            self.staffdict[newstaff].append('H')
            print('Congratulations. ' + newstaff +
                  ' is the new head librarian.')
                  
    def removestaff(self, removestaff, headlibrarian):
        if self.staffdict:
            if removestaff in self.staffdict.keys():
                for staffmember in self.staffdict.keys():
                    if len(self.staffdict[staffmember]) > 4:
                        if staffmember == headlibrarian:
                            del self.staffdict[removestaff]
                            del self.memberdict[removestaff]
                            print('This staff member has been removed from the library.')
                        else:
                            print('You are not the head librarian, so you cannot remove a staff member.')
            else:
                print('This person is not a staff member.')
        else:
            print('There are no staff members in the library yet.')

class library(staff):
    def __init__(self):
        address.__init__(self)
        staff.__init__(self)
    
    def closelibrary(self):
        print("Writing pickle file...")
        with open("testpickle", "wb") as f:
            pickle.dump(self.bookdict, f)
        print("Pickle file {} has been written.".format("testpickle"))   
            
            

mylibrary = library()
mylibrary.loadbooks('books.csv')
mylibrary.printlib()
mylibrary.closelibrary()

'''
#main code
mylibrary.addstaff('Udbhav')
mylibrary.addstaff('Venky', 'Udbhav')
mylibrary.removemember('Venky', 'Udbhav')
mylibrary.inputbook('Hello World', 'Udbhav')
mylibrary.checkoutbook('Hello World', 'Udbhav')
mylibrary.returnbook('Hello World', 'Udbhav')
'''       
        