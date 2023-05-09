import wallet
import account


def setup():

    print("Setting up a few accounts to get you started...\n")
    profile_one = wallet.Customer.from_list(
        ['Daniel Shrestha', '02/07/2002', 'Pulchowk', '9841400050', 'd.shrestha@gmail.com'])
    profile_two = wallet.Customer.from_list(
        ['Sradda Shahi', '05/05/1997', 'Koteshwor', '9803399781', 's.shahi@gmail.com'])
    profile_three = wallet.Customer.from_list(
        ['Anuja Pandey', '14/11/1999', 'New Road', '9802122221', 'a.pandey@gmail.com'])

    profile_one_txn = wallet.NewAccount(profile_one.usr_id, 1500)
    profile_two_txn = wallet.NewAccount(profile_two.usr_id, 1500)
    profile_three_txn = wallet.NewAccount(profile_three.usr_id, 1500)


def runtest():

    try:

        print("Starting the TEST by registering a new user and creating user profile.\n")

        new_profile = wallet.Customer.from_list(
            ['Jenny Wallace', '03/09/2003', 'Oldenberg', '9841420082', 'j.wallace@gmail.com'])
        user_session = wallet.Customer(new_profile.usr_id)

        print("\nViewing User profile details:\n")
        user_session.view_profile()
        print("\nUpdating the user Address to :'Baneshwor-KTM'")
        user_session.update_profile("Address", 'Baneshwor-KTM')
        print("\nViewing user profile details after updating address:\n")
        user_session.view_profile()
        print("\nUpdating the user phone number to :9851011121")
        user_session.update_profile("Phone", "9851011121")
        print("\nViewing user profile details after updating phone number:\n")
        user_session.view_profile()
        print("\nProceeding to create a new transaction account for our user with Rs. 1500 starting balance.\n")
        usr_acc = wallet.NewAccount(new_profile.usr_id, 1500)

        print("\nCreating two more user profiles and transaction accounts with Rs. 1500 starting balance each.\n")
        new_profile_two = wallet.Customer.from_list(
            ['Lara Smith', '02/02/1997', 'Hannover', '9869127543', 'l.nelde@gmail.com'])
        new_profile_three = wallet.Customer.from_list(
            ['Sami Hasan', '07/09/1994', 'Karachi', '9847443351', 's.seth@gmail.com'])
        usr_acc_two = wallet.NewAccount(new_profile_two.usr_id, 1500)
        usr_acc_three = wallet.NewAccount(new_profile_three.usr_id, 1500)

        print("\nNow *** TESTING YOUR CODE *** on the Account class for the first user!")
        acc_session = account.Account(new_profile.usr_id)
        print("\nViewing account details.")
        acc_session.view_account_details()
        print("\nViewing balance in the account.")
        print("The balance is: ", acc_session.view_balance())
        print("\nDeposit Rs 100 in the account.\n")
        acc_session.deposit(100)

        if int(acc_session.view_balance()) != 1600:
            print("TEST FAILED!!")
            return None
        print("\nWithdraw Rs 50 from the account.")
        acc_session.withdraw(50)

        if int(acc_session.view_balance()) != 1550:
            print("TEST FAILED!!")
            return None

        print("\nTry to overdraw the account. Attempt to withdraw 5000")
        acc_session.withdraw(5000)

        if float(acc_session.view_balance()) < 0:
            print("TEST FAILED!!")
            return None

        UID_FRIEND = 1003
        print(f"\nTransfer Rs 9000 to a friend with user ID {UID_FRIEND}.")
        acc_session.transfer_funds(1003, 9000)

        print(f"\nTransfer Rs 333 to a friend with user ID {UID_FRIEND}.")
        friend_acc = account.Account(UID_FRIEND)
        old_balance_friend = float(friend_acc.view_balance())
        old_balance_user = float(acc_session.view_balance())
        acc_session.transfer_funds(UID_FRIEND, 333)
        if (old_balance_user - float(acc_session.view_balance())) != (float(friend_acc.view_balance())-old_balance_friend):
            print("TEST FAILED!!")
            return None

        print("\nPreliminary tests ran successfully!! YOU PASSED THE FIRST TASK! Only two more to go!!\n")
    except:
        print("TEST FAILED!!")


if __name__ == '__main__':
    runtest()
    
