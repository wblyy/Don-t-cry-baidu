from mydb import myuserdb, xiaomidb

def main():
    usersdb = myuserdb()
    xmdb = xiaomidb()
    with open('./hashcat-0.47/xiaomi_passwd/xiaomi_aa', 'r') as f:
        for line in f:
            row = line.strip('\n').split(':')
            passwd_hash = row[0]+":"+row[1]
            passwd_text = row[2]
            rc = xmdb.get_user_by_passwd(passwd_hash)
            print rc[0], passwd_text, rc[1]
            usersdb.add_user(rc[0], passwd_text, rc[1])


if __name__ == "__main__":
    main()
