from datetime import datetime

def match_date(myDate):
    try:
        # we only have a date? 
        if len(myDate.split(' ')) == 1:
            try:
                myDObj = datetime.strptime(myDate, '%d-%b-%Y')
                # return date object in form "DD-MM-YYY"
                return(myDObj)
            except Exception as ie:
                print("Error dateonly :", ie)
                print("For date only please provide date in the format 'DD-Mon-YYYY'")
                return(False)
        elif len(myDate.split(' ')) == 2:
            try:
                # try to split the time based on the : (string -1 to remove a may ending : e.g.: 04: = 04)
                if len(myDate.split(' ')[1][:-1].split(':')) == 1:
                    # return date object in form "DD-MM-YYY HH24"
                    try:
                        myDObj = datetime.strptime(myDate, '%d-%b-%Y %H')
                    except ValueError:
                        myDObj = datetime.strptime(myDate, '%d-%b-%Y %H:')
                    return(myDObj)
                elif len(myDate.split(' ')[1][:-1].split(':')) == 2:
                    # return date object in form "DD-MM-YYY HH24:MI"
                    try:
                        myDObj = datetime.strptime(myDate, '%d-%b-%Y %H:%M')
                    except ValueError:
                        myDObj = datetime.strptime(myDate, '%d-%b-%Y %H:%M:')
                    return(myDObj)
                elif len(myDate.split(' ')[1][:-1].split(':')) == 3:
                    # return date object in form "DD-MM-YYY HH24:MI:SS"
                    try:
                        myDObj = datetime.strptime(myDate, '%d-%b-%Y %H:%M:%S')
                    except ValueError:
                        myDObj = datetime.strptime(myDate, '%d-%b-%Y %H:%M:%S:')
                    return(myDObj)
            except Exception as ie:
                print("Error date-time :", ie)
                print("Date-Time format should be in the format:")
                print("   -> 'DD-Mon-YYYY HH24'")
                print("   -> 'DD-Mon-YYYY HH24:MI'")
                print("   -> 'DD-Mon-YYYY HH24:MI:SS'")
                return(False)
        else:
            print("Date not recognized")
            return(False)

    except Exception as oe:
        print("No date string given I suppose:", oe)
        return(False)

print(match_date('17-Oct-2020 13:9:1'))
            
