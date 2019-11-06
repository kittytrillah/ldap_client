import ssl

LDAP_SERVER = 'ldap.secne.space'
LDAP_PORT = 636
LDAP_BINDDN = 'cn=admin,dc=secne,dc=space'
LDAP_CONNECT_TIMEOUT = 10  # Honored when the TCP connection is being established
LDAP_USE_TLS = True  # default
LDAP_REQUIRE_CERT = ssl.CERT_NONE  # default: CERT_REQUIRED
LDAP_TLS_VERSION = ssl.PROTOCOL_TLSv1_2  # default: PROTOCOL_TLSv1
LDAP_CERT_PATH = '/etc/openldap/certs'