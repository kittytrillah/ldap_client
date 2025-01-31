import ldap3 as ldap
from ldap3 import Server, Connection, ALL, SIMPLE, MODIFY_REPLACE
from ldap3.core.tls import Tls
from ldap3.core.exceptions import LDAPSocketOpenError
import security

credentials = []




def ldap3_connection(address, dn, password, port_n, ssl):
    global credentials
    fail = False
    credentials = [address, dn, password, port_n, ssl]
    port_i = int(port_n)
    server = Server(address, port=port_i, use_ssl=ssl, get_info=ALL)
    try:
        conn = Connection(server, user=dn, password=password, raise_exceptions=True, authentication=SIMPLE)
        conn.start_tls()
        print(">>>LDAP Bind Successful. ")
        conn.open()
        conn.bind()
    except:
        print('LDAP Bind Failed')
        m = 'fail'
        fail = True
        return m
    # except ldap.core.exceptions.LDAPInvalidCredentialsResult as e:
    finally:
        if fail:
            return m
        else:
            return conn


def get_schema(o_c):
    conn = ldap3_connection(credentials[0], credentials[1], credentials[2], credentials[3], credentials[4])
    if len(o_c) != 0:
        schema_res = conn.server.schema.object_classes[o_c]
        return schema_res
    else:
        schema_res = conn.server.schema
        return schema_res


def mod(user_dn, sn, telephone_number, description, cn, c, old_pass, new_pass):
    conn = ldap3_connection(c[0], c[1], c[2], c[3], c[4])
    if len(sn) != 0:
        conn.modify(user_dn,
                    {'sn': [(MODIFY_REPLACE, [sn])]})
    if len(telephone_number):
        conn.modify(user_dn,
                    {'telephoneNumber': [(MODIFY_REPLACE, [telephone_number])]})
    if len(description):
        conn.modify(user_dn,
                    {'description': [(MODIFY_REPLACE, [description])]})
    if len(old_pass) != 0 and len(new_pass) != 0:
        old_pass_h = security.encrypt(old_pass)
        new_pass_h = security.encrypt(new_pass)
        try:
            ldap.extend.microsoft.modifyPassword.ad_modify_password(conn, user_dn, new_pass_h, old_pass_h, controls=None)
        except:
            print("Error - password incorrect")
    conn.unbind()


def display(addr, dn, pwd, attr, obj_class):
    conn = ldap3_connection(addr, dn, pwd, credentials[3],credentials[4])
    if len(obj_class) != 0:
        conn.search('dc=secne,dc=space', search_filter='(&(objectclass=' + str(obj_class) + '))', attributes=attr)  # , paged_size=5
        return conn.entries
    else:
        conn.search('dc=secne,dc=space', search_filter='(&(objectclass=*))', attributes=attr)  # , paged_size=5
        return conn.entries
    conn.unbind()



def add(new_user, sn, telephone_number, description, cn, c, pwd):
    conn = ldap3_connection(c[0], c[1], c[2], c[3], c[4])
    try:
        conn.add(new_user, attributes={'objectClass': ['person', 'top'],
                                    'sn': sn,
                                    'cn': cn,
                                    'telephoneNumber': telephone_number,
                                    'description': description,
                                    'userPassword': pwd
                                    })
        print(">>>user Added Successfully!")
        conn.search('dc=secne,dc=space', search_filter=f'(&(objectclass=*)(sn={sn}))', attributes=['cn', 'sn', 'objectClass', 'telephoneNumber', 'userPassword'])
        print(conn.entries)
        conn.unbind()
    except Exception as e:
        print("user not added : ", e)


def delete_entry(cn):
    conn = ldap3_connection(credentials[0], credentials[1], credentials[2], credentials[3], credentials[4])
    conn.delete(cn)
    conn.unbind()