import csv
import pandas as pd

TRANSACTION_RECORDS = 'account_transactions.csv'
USER_RECORDS = 'user_records.csv'

class Customer:

    '''This class helps create a new Customer ID and profile if one does not already exist. It also offers other funtionalities to pre-existing users.

    Usage:

        Option 1 > myprofile = Customer(UserID) 
        Option 2 > myprofile = Customer.from_list([.,.,.])
        Option 3 > myprofile = Customer.from_keyboard()

    Returns:
        A new user account and/or user profile.

    Example 1:
        myprofile = Customer(1001)

        > Access an already existing User account and profile (if applicable) with UserID 1001.

    Example 2:
        yourprofile = Customer.from_list(['Joe Doe', 02/01/1993,'NYC',01577777,j.doe@mail.com])

        > Register a new user Joe Doe and return a new user account with some UserID. User attributes passed as a list.

    Example 3:
        theirprofile = Customer.from_keyboard()

        > Register a new user and return a new user account with some UserID. User attributes passed through the standard IO (keyboard).

    '''

    _fields = ("UserID", "Name", "DOB", "Address", "Phone", "Email")

    def __init__(self, usr_id=None, user_info_list=[]):

        self.usr_id = usr_id
        self._attributes = user_info_list

        assert usr_id or user_info_list, "User ID required!"

        if not self.usr_id:
            self.usr_id = self._create_new_id()
        if self._check_existing_id() == False:
            print("User ID not recognized. Consider creating a new user account!")

    @classmethod
    def from_list(cls, values):
        return cls(None, values)

    @classmethod
    def from_keyboard(cls):

        print("Please fill in your details to continue using the app.")
        values = []
        for i in cls._fields[1:]:
            usr_in = input("Please enter {}: ".format(i))
            values.append(usr_in)
        return cls(None, values)

    def _create_user_profile(self, uid):

        values = [uid]
        if self._attributes:
            for i in self._attributes:
                values.append(i)
            return values

    def _check_existing_id(self, usr_id=None):

        if not usr_id:
            usr_id = self.usr_id
        try:
            with open(USER_RECORDS, 'r') as file:
                reader = csv.reader(file)
                next(reader)
                for row in reader:
                    if int(row[0]) == int(usr_id):
                        return True
            return False

        except FileNotFoundError as e:
            print(f"Check if file available. Following error occured: {e}")
            raise KeyboardInterrupt

    def _generate_id_token(self):

        try:
            with open(USER_RECORDS, 'r') as file:
                reader = csv.reader(file)
                next(reader)
                t = [row[0] for row in reader if row]
                count = t[-1] if len(t) != 0 else 1000
                try:
                    new_id_token = int(count) + 1
                    if not self._check_existing_id(new_id_token):
                        return new_id_token

                except ValueError as e:
                    print(
                        f"Problem in user records file. Following error occured: {e}")
                    raise KeyboardInterrupt

        except FileNotFoundError as e:
            print(f"Check if file available. Following error occured: {e}")
            raise KeyboardInterrupt

    def _create_new_id(self):

        try:
            self.usr_id = self._generate_id_token()

            assert self.usr_id != None, "UID cannot be none. please try again."

            print("User ID generated for user. UserID is:{}. Filling in the user details as provided.".format(
                self.usr_id))

            profile_details = self._create_user_profile(self.usr_id)

            assert profile_details != None, "Empty user records, UserID creation failed. Please contact the support team."

            try:
                with open(USER_RECORDS, 'a+', newline='') as f:
                    writer = csv.writer(f, delimiter=',')
                    writer.writerow(profile_details)
            except Exception as e:
                print(
                    "Following error occurred during writing to records: {}. Please contact the support team.".format(e))
                raise KeyboardInterrupt

            return self.usr_id

        except AssertionError as e:
            print(e)
            raise KeyboardInterrupt

    def view_profile(self):

        def fetch_user_info():
            with open(USER_RECORDS, 'r') as file:
                reader = csv.reader(file)
                next(reader)
                for row in reader:
                    if row:
                        if int(row[0]) == int(self.usr_id):
                            return dict(zip(self._fields[1:], row[1:]))
            return ("Error accessing profile. Contact support.")

        try:
            for keys, values in fetch_user_info().items():
                print("{:7} : {}".format(keys, values))

        except Exception as e:
            print("Profile info not available. Error code: {}".format(e))

    def update_profile(self, field, value):
        try:
            if field in self._fields:
                df = pd.read_csv(USER_RECORDS, delimiter=',')
                df.loc[df[self._fields[0]] == self.usr_id, field] = str(value)
                df.to_csv(USER_RECORDS, index=False)
                print("User(UID: {})'s {} updated successfully to {}!".format(
                    self.usr_id, field, value))
            else:
                print("Unidentified field value!!")
        except Exception as e:
            print("Following error occurred during writing to records: {}. Please contact the support team.".format(e))


class NewAccount:

    '''This class creates a new transaction account if no account is present. A UserID is first needed to be able to create a new account. The User ID 
    can be generated from the Customer class. Once UserID has been generated from the Customer class, an account can be created here using the same UserID.

    Usage:

        uid = 1000
        starting_balance = Rs. 15000  (optional)
        myaccount = NewAccount(uid,starting_balance)

    Returns:
        A new user account with specified balance.

    Note:
        Balance is optional. The default balance is Rs. 1.

    Example 1:
        myaccount = NewAccount(1000,11000)

        > This returns an account with available balance of Rs 11000.

    Example 2:
        myaccount = NewAccount(1001)

        > This returns an account with available balance of Rs 1.

    '''

    def __init__(self, usr_id, balance=1):
        self.usr_id = usr_id
        self.balance = balance
        self._account = None
        self.acc_details = self._create_account(self.balance)

    def _check_existing_id(self):
        try:
            with open(USER_RECORDS, 'r') as file:
                reader = csv.reader(file)
                next(reader)
                for row in reader:
                    if row:
                        if int(row[0]) == int(self.usr_id):
                            return True
            return False

        except FileNotFoundError as e:
            print(f"Check if file available. Following error occured: {e}")
            raise KeyboardInterrupt

    def _check_previous_accounts(self):

        try:
            with open(TRANSACTION_RECORDS, 'r') as file:
                reader = csv.reader(file)
                next(reader)
                for row in reader:
                    if row:
                        if int(row[0]) == int(self.usr_id):
                            return True
            return False
        except FileNotFoundError as e:
            print(f"Check if file available. Following error occured: {e}")
            raise KeyboardInterrupt

    def _generate_account_number(self):

        try:
            with open(TRANSACTION_RECORDS, 'r') as file:
                reader = csv.reader(file)
                next(reader)
                t = [row[1] for row in reader if row]
                last_val = t[-1] if len(t) != 0 else 330000001
                try:
                    ac_num = int(last_val) + 1
                    return ac_num
                except ValueError as e:
                    print(
                        f"Problem in transaction records file. Following error occured: {e}")
                    raise KeyboardInterrupt

        except FileNotFoundError as e:
            print(f"Check if file available. Following error occured: {e}")
            raise KeyboardInterrupt

    def _create_account(self, initial_balance=1):

        if self._check_existing_id() == False:
            print("User ID: {} not found in records! ".format(self.usr_id))
        else:
            if self._check_previous_accounts() == True:
                print("Account for user ID: {} already exists! ".format(self.usr_id))

            elif self._check_previous_accounts() == False:
                self._account, self.balance = self._generate_account_number(), initial_balance

                try:
                    assert self._account != None, "Useraccount has not been created."
                    usr_data = [self.usr_id, self._account, self.balance]
                    try:
                        with open(TRANSACTION_RECORDS, 'a+', newline='') as f:
                            writer = csv.writer(f, delimiter=',')
                            writer.writerow(usr_data)
                        print("Account Created Successfully!! Account number is: {} with available balance: {}".format(
                            self._account, self.balance))
                    except Exception as e:
                        print(
                            "Following error occurred during writing to records: {}. Please contact the support team.".format(e))
                        raise KeyboardInterrupt
                except AssertionError as e:
                    print(e)
                    raise KeyboardInterrupt

                except Exception as e:
                    print("Error:{}".format(e))

        return {"User ID": self.usr_id, "Account Number": self._account, "Starting Balance": self.balance}
