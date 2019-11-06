# ldap_client
Simple LDAP client with database and flask


Functions:
1. Get schema
2. Search by criteria
3. Add entry
4. Modify entry
5. Remove entry


Usage:
1. Run the server
2. Follow the GUI
3. dn should look like -> cn=username,dc=domain,dc=com
4. You can save credentials by clicking "Remember me". Password will be stored as sha-512 hash. 
5. If you saved your credentials, you can simply input password and connect.
6. Everything else is understandeable from GUI


Known bugs:
1. After operations of addition, entry form doesn't return to index page
2. Sometimes issues with connecting



Viktor Zaika/2019 
UniNE, assignment
