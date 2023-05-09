import csv

TRANSACTION_RECORDS = 'account_transactions.csv'
USER_RECORDS = 'user_records.csv'


class Account:

    _attributes = ("UID", "Account Number", "Balance")

    def __init__(self, usr_id, acc_number=None):

        self.usr_id = usr_id
        self.acc_number = acc_number
        if self.acc_number is None:
            self.acc_number = self._get_account_number()

    def _get_account_number(self, uid=None):

        if not uid:
            uid = self.usr_id
        with open(TRANSACTION_RECORDS, 'r') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                if row:
                    if int(row[0]) == int(uid):
                        return row[1]
        print("Account not found. Please create a new account using the newAccount option.")

    def view_account_details(self):

        with open(TRANSACTION_RECORDS, 'r') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                if row:
                    if int(row[0]) == int(self.usr_id):
                        details = dict(zip(self._attributes[1:], row[1:]))

        for keys, values in details.items():
            print("{} : {}".format(keys, values))

    def view_balance(self, uid=None):

        if not uid:
            uid = self.usr_id

        with open(TRANSACTION_RECORDS, 'r') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                if row:
                    if int(row[0]) == int(uid):
                        return row[2]
        print("Error occurred. Please contact support.")
        return None

    def deposit(self, amount):
        try:
            with open ("account_transactions.csv", 'r+', newline='') as file:
                reader = csv.reader(file)
                next(reader) 
                rows = list(reader)
                if not rows:
                    print("There are no transaction records.")
                    return
                for row in rows:
                    if row and int(row[0]) == int(self.usr_id):
                        current_balance = int(row[2])
                        updated_balance = current_balance + amount
                        row[2] = updated_balance
                        file.seek(0)
                        file.truncate()
                        writer = csv.writer(file)
                        writer.writerow(['UID', 'ACNumber', 'Balance'])
                        writer.writerows(rows)
                        break
                else:
                    print("Account not found.")
                    return

            print(f"Deposited: Rs. {amount}")
            print(f"Updated Balance: Rs. {updated_balance}")
            
        except Exception as e:
            print("e")
            
    def withdraw(self, amount):
        try:
            with open("account_transactions.csv", 'r+', newline='') as file:
                reader = csv.reader(file)
                next(reader) 
                rows = list(reader)
                if not rows:
                    print("There are no transaction records.")
                    return
                for row in rows:
                    if row and int(row[0]) == int(self.usr_id):   
                        current_balance = int(row[2])
                        if amount <= current_balance:
                            updated_balance = current_balance - amount
                            row[2] = updated_balance
                            file.seek(0)
                            file.truncate()
                            writer = csv.writer(file)
                            writer.writerow(['UID', 'ACNumber', 'Balance'])
                            writer.writerows(rows)

                            break
                        else:
                            print("Insufficient balance.")
                            return
                else:
                    print("Account not found.")
                    return

            print(f"Withdrawn: Rs. {amount}")
            print(f"Updated Balance: Rs. {updated_balance}")
            
        except Exception as e:
            print("e")
            
    def transfer_funds(self, uid, amount):
        try:
            with open("account_transactions.csv", 'r+', newline='') as file:
                reader = csv.reader(file)
                next(reader)
                rows = list(reader)
                if not rows:
                    print("There are no transaction records.")
                    return
                from_account_found = False
                to_account_found = False
                for row in rows:
                    if row and int(row[0]) == int(self.usr_id):
                        current_balance = int(row[2])
                        if amount <= current_balance:
                            updated_balance = current_balance - amount
                            row[2] = updated_balance
                            from_account_found = True
                            break
                        else:
                            print("Insufficient balance.")
                            return
                else:
                    print("Account not found.")
                    return

                for row in rows:
                    if row and int(row[0]) == int(uid):
                        current_balance = int(row[2])
                        update_balance = current_balance + amount
                        row[2] = update_balance
                        to_account_found = True
                        break
                        
                
                if not from_account_found:
                    print("User account not found.")
                    return

                if not to_account_found:
                    print("Beneficiary account not found.")
                    return

                file.seek(0)
                file.truncate()
                writer = csv.writer(file)
                writer.writerow(['UID', 'ACNumber', 'Balance'])
                writer.writerows(rows)


            print(f"Transferred: Rs. {amount} from account number {self.usr_id} to UID {uid}")
            print(f"Updated Balance for UID {self.usr_id}: Rs. {updated_balance}")
            print(f"Updated Balance for UID {uid}: Rs. {update_balance}")
            
        except Exception as e:
            print("e")
