#!/usr/bin/python
# 
import sys, getopt, ldap3, os

def dumpldap(ip, port, ssl, domain, ofile='', user='', pwd=''):
    if ssl == "True":
        ssl = True
    else:
        ssl = False
    server = ldap3.Server(ip, get_info=ldap3.ALL, port=port, use_ssl=ssl)
    connection = ldap3.Connection(server, user=user, password=pwd)
    if connection.bind():
        try:
            if connection.search(search_base=domain, search_scope='SUBTREE', attributes='*', search_filter='(&(objectClass=person))'):
                if ofile == "":
                    print(connection.entries)
                else:
                    f = open(ofile, 'w')
                    f.write(str(connection.entries))
                    f.close()
        except:
            print("ERROR: Check the domain")
            usage()
            sys.exit(2)
    else:
        print(connection.last_error)

def usage():
    print(os.path.basename(__file__) + ' -d <domain> -i <ip> -p <Port> -s <True|False> -o <outputfile>')
    print(os.path.basename(__file__) + ' --domain <domain> --ip <ip> --port <Port> --ssl <True|False> --ofile <outputfile>')
    print(os.path.basename(__file__) + ' -d "DC=MYDOMAIN,DC=LOCAL" -i 192.168.0.1 -p 389 -s False -o MyLdapDump')

def main(argv):
    domain = ''
    port = ''
    ip = ''
    ssl = False
    ofile = ''
    user=''
    pwd=''
    try:
        opts, args = getopt.getopt(argv,"hd:p:i:s:o:u:P:",["domain=","port=", "ip=", "ssl=", "ofile=", "user=", "password="])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            usage()
            sys.exit()
        elif opt in ("-d", "--domain"):
            domain = arg
        elif opt in ("-i", "--ip"):
            ip = arg
        elif opt in ("-p", "--port"):
            port = arg
        elif opt in ("-s", "--ssl"):
            ssl = arg
        elif opt in ("-o", "--ofile"):
            ofile = arg
        elif opt in ("-u", "--user"):
            user = arg
        elif opt in ("-P", "--password"):
            pwd = arg

    if domain != "" and ip != "" and port != "" and ssl != "":
        dumpldap(ip, int(port), ssl, domain, ofile, user, pwd)
    else:
        print("Missing arguments")
        usage()
        sys.exit(2)

if __name__ == "__main__":
    main(sys.argv[1:])
