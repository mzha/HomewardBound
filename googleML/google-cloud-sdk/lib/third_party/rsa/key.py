# -*- coding: utf-8 -*-
#
#  Copyright 2011 Sybren A. Stüvel <sybren@stuvel.eu>
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

'''RSA key generation code.

Create new keys with the newkeys() function. It will give you a PublicKey and a
PrivateKey object.

Loading and saving keys requires the pyasn1 module. This module is imported as
late as possible, such that other functionality will remain working in absence
of pyasn1.

'''

import logging
from rsa._compat import b, bytes_type

import rsa.pem
import rsa.common

log = logging.getLogger(__name__)



class AbstractKey(object):
    '''Abstract superclass for private and public keys.'''

    @classmethod
    def load_pkcs1(cls, keyfile, format='PEM'):
        r'''Loads a key in PKCS#1 DER or PEM format.

        :param keyfile: contents of a DER- or PEM-encoded file that contains
            the public key.
        :param format: the format of the file to load; 'PEM' or 'DER'

        :return: a PublicKey object

        '''

        methods = {
            'PEM': cls._load_pkcs1_pem,
            'DER': cls._load_pkcs1_der,
        }

        if format not in methods:
            formats = ', '.join(sorted(methods.keys()))
            raise ValueError('Unsupported format: %r, try one of %s' % (format,
                formats))

        method = methods[format]
        return method(keyfile)

    def save_pkcs1(self, format='PEM'):
        '''Saves the public key in PKCS#1 DER or PEM format.

        :param format: the format to save; 'PEM' or 'DER'
        :returns: the DER- or PEM-encoded public key.

        '''

        methods = {
            'PEM': self._save_pkcs1_pem,
            'DER': self._save_pkcs1_der,
        }

        if format not in methods:
            formats = ', '.join(sorted(methods.keys()))
            raise ValueError('Unsupported format: %r, try one of %s' % (format,
                formats))

        method = methods[format]
        return method()

class PublicKey(AbstractKey):
    '''Represents a public RSA key.

    This key is also known as the 'encryption key'. It contains the 'n' and 'e'
    values.

    Supports attributes as well as dictionary-like access. Attribute accesss is
    faster, though.

    >>> PublicKey(5, 3)
    PublicKey(5, 3)

    >>> key = PublicKey(5, 3)
    >>> key.n
    5
    >>> key['n']
    5
    >>> key.e
    3
    >>> key['e']
    3

    '''

    __slots__ = ('n', 'e')

    def __init__(self, n, e):
        self.n = n
        self.e = e

    def __getitem__(self, key):
        return getattr(self, key)

    def __repr__(self):
        return 'PublicKey(%i, %i)' % (self.n, self.e)

    def __eq__(self, other):
        if other is None:
            return False

        if not isinstance(other, PublicKey):
            return False

        return self.n == other.n and self.e == other.e

    def __ne__(self, other):
        return not (self == other)

    @classmethod
    def _load_pkcs1_der(cls, keyfile):
        r'''Loads a key in PKCS#1 DER format.

        @param keyfile: contents of a DER-encoded file that contains the public
            key.
        @return: a PublicKey object

        First let's construct a DER encoded key:

        >>> import base64
        >>> b64der = 'MAwCBQCNGmYtAgMBAAE='
        >>> der = base64.decodestring(b64der)

        This loads the file:

        >>> PublicKey._load_pkcs1_der(der)
        PublicKey(2367317549, 65537)

        '''

        from pyasn1.codec.der import decoder
        from rsa.asn1 import AsnPubKey
        
        (priv, _) = decoder.decode(keyfile, asn1Spec=AsnPubKey())
        return cls(n=int(priv['modulus']), e=int(priv['publicExponent']))

    def _save_pkcs1_der(self):
        '''Saves the public key in PKCS#1 DER format.

        @returns: the DER-encoded public key.
        '''

        from pyasn1.codec.der import encoder
        from rsa.asn1 import AsnPubKey

        # Create the ASN object
        asn_key = AsnPubKey()
        asn_key.setComponentByName('modulus', self.n)
        asn_key.setComponentByName('publicExponent', self.e)

        return encoder.encode(asn_key)

    @classmethod
    def _load_pkcs1_pem(cls, keyfile):
        '''Loads a PKCS#1 PEM-encoded public key file.

        The contents of the file before the "-----BEGIN RSA PUBLIC KEY-----" and
        after the "-----END RSA PUBLIC KEY-----" lines is ignored.

        @param keyfile: contents of a PEM-encoded file that contains the public
            key.
        @return: a PublicKey object
        '''

        der = rsa.pem.load_pem(keyfile, 'RSA PUBLIC KEY')
        return cls._load_pkcs1_der(der)

    def _save_pkcs1_pem(self):
        '''Saves a PKCS#1 PEM-encoded public key file.

        @return: contents of a PEM-encoded file that contains the public key.
        '''

        der = self._save_pkcs1_der()
        return rsa.pem.save_pem(der, 'RSA PUBLIC KEY')

    @classmethod
    def load_pkcs1_openssl_pem(cls, keyfile):
        '''Loads a PKCS#1.5 PEM-encoded public key file from OpenSSL.
        
        These files can be recognised in that they start with BEGIN PUBLIC KEY
        rather than BEGIN RSA PUBLIC KEY.
        
        The contents of the file before the "-----BEGIN PUBLIC KEY-----" and
        after the "-----END PUBLIC KEY-----" lines is ignored.

        @param keyfile: contents of a PEM-encoded file that contains the public
            key, from OpenSSL.
        @return: a PublicKey object
        '''

        der = rsa.pem.load_pem(keyfile, 'PUBLIC KEY')
        return cls.load_pkcs1_openssl_der(der)

    @classmethod
    def load_pkcs1_openssl_der(cls, keyfile):
        '''Loads a PKCS#1 DER-encoded public key file from OpenSSL.

        @param keyfile: contents of a DER-encoded file that contains the public
            key, from OpenSSL.
        @return: a PublicKey object
        '''
    
        from rsa.asn1 import OpenSSLPubKey
        from pyasn1.codec.der import decoder
        from pyasn1.type import univ
        
        (keyinfo, _) = decoder.decode(keyfile, asn1Spec=OpenSSLPubKey())
        
        if keyinfo['header']['oid'] != univ.ObjectIdentifier('1.2.840.113549.1.1.1'):
            raise TypeError("This is not a DER-encoded OpenSSL-compatible public key")
                
        return cls._load_pkcs1_der(keyinfo['key'][1:])
        
        


class PrivateKey(AbstractKey):
    '''Represents a private RSA key.

    This key is also known as the 'decryption key'. It contains the 'n', 'e',
    'd', 'p', 'q' and other values.

    Supports attributes as well as dictionary-like access. Attribute accesss is
    faster, though.

    >>> PrivateKey(3247, 65537, 833, 191, 17)
    PrivateKey(3247, 65537, 833, 191, 17)

    exp1, exp2 and coef don't have to be given, they will be calculated:

    >>> pk = PrivateKey(3727264081, 65537, 3349121513, 65063, 57287)
    >>> pk.exp1
    55063
    >>> pk.exp2
    10095
    >>> pk.coef
    50797

    If you give exp1, exp2 or coef, they will be used as-is:

    >>> pk = PrivateKey(1, 2, 3, 4, 5, 6, 7, 8)
    >>> pk.exp1
    6
    >>> pk.exp2
    7
    >>> pk.coef
    8

    '''

    __slots__ = ('n', 'e', 'd', 'p', 'q', 'exp1', 'exp2', 'coef')

    def __init__(self, n, e, d, p, q, exp1=None, exp2=None, coef=None):
        self.n = n
        self.e = e
        self.d = d
        self.p = p
        self.q = q

        # Calculate the other values if they aren't supplied
        if exp1 is None:
            self.exp1 = int(d % (p - 1))
        else:
            self.exp1 = exp1

        if exp1 is None:
            self.exp2 = int(d % (q - 1))
        else:
            self.exp2 = exp2

        if coef is None:
            self.coef = rsa.common.inverse(q, p)
        else:
            self.coef = coef

    def __getitem__(self, key):
        return getattr(self, key)

    def __repr__(self):
        return 'PrivateKey(%(n)i, %(e)i, %(d)i, %(p)i, %(q)i)' % self

    def __eq__(self, other):
        if other is None:
            return False

        if not isinstance(other, PrivateKey):
            return False

        return (self.n == other.n and
            self.e == other.e and
            self.d == other.d and
            self.p == other.p and
            self.q == other.q and
            self.exp1 == other.exp1 and
            self.exp2 == other.exp2 and
            self.coef == other.coef)

    def __ne__(self, other):
        return not (self == other)

    @classmethod
    def _load_pkcs1_der(cls, keyfile):
        r'''Loads a key in PKCS#1 DER format.

        @param keyfile: contents of a DER-encoded file that contains the private
            key.
        @return: a PrivateKey object

        First let's construct a DER encoded key:

        >>> import base64
        >>> b64der = 'MC4CAQACBQDeKYlRAgMBAAECBQDHn4npAgMA/icCAwDfxwIDANcXAgInbwIDAMZt'
        >>> der = base64.decodestring(b64der)

        This loads the file:

        >>> PrivateKey._load_pkcs1_der(der)
        PrivateKey(3727264081, 65537, 3349121513, 65063, 57287)

        '''

        from pyasn1.codec.der import decoder
        (priv, _) = decoder.decode(keyfile)

        # ASN.1 contents of DER encoded private key:
        #
        # RSAPrivateKey ::= SEQUENCE {
        #     version           Version, 
        #     modulus           INTEGER,  -- n
        #     publicExponent    INTEGER,  -- e
        #     privateExponent   INTEGER,  -- d
        #     prime1            INTEGER,  -- p
        #     prime2            INTEGER,  -- q
        #     exponent1         INTEGER,  -- d mod (p-1)
        #     exponent2         INTEGER,  -- d mod (q-1) 
        #     coefficient       INTEGER,  -- (inverse of q) mod p
        #     otherPrimeInfos   OtherPrimeInfos OPTIONAL 
        # }

        if priv[0] != 0:
            raise ValueError('Unable to read this file, version %s != 0' % priv[0])

        as_ints = tuple(int(x) for x in priv[1:9])
        return cls(*as_ints)

    def _save_pkcs1_der(self):
        '''Saves the private key in PKCS#1 DER format.

        @returns: the DER-encoded private key.
        '''

        from pyasn1.type import univ, namedtype
        from pyasn1.codec.der import encoder

        class AsnPrivKey(univ.Sequence):
            componentType = namedtype.NamedTypes(
                namedtype.NamedType('version', univ.Integer()),
                namedtype.NamedType('modulus', univ.Integer()),
                namedtype.NamedType('publicExponent', univ.Integer()),
                namedtype.NamedType('privateExponent', univ.Integer()),
                namedtype.NamedType('prime1', univ.Integer()),
                namedtype.NamedType('prime2', univ.Integer()),
                namedtype.NamedType('exponent1', univ.Integer()),
                namedtype.NamedType('exponent2', univ.Integer()),
                namedtype.NamedType('coefficient', univ.Integer()),
            )

        # Create the ASN object
        asn_key = AsnPrivKey()
        asn_key.setComponentByName('version', 0)
        asn_key.setComponentByName('modulus', self.n)
        asn_key.setComponentByName('publicExponent', self.e)
        asn_key.setComponentByName('privateExponent', self.d)
        asn_key.setComponentByName('prime1', self.p)
        asn_key.setComponentByName('prime2', self.q)
        asn_key.setComponentByName('exponent1', self.exp1)
        asn_key.setComponentByName('exponent2', self.exp2)
        asn_key.setComponentByName('coefficient', self.coef)

        return encoder.encode(asn_key)

    @classmethod
    def _load_pkcs1_pem(cls, keyfile):
        '''Loads a PKCS#1 PEM-encoded private key file.

        The contents of the file before the "-----BEGIN RSA PRIVATE KEY-----" and
        after the "-----END RSA PRIVATE KEY-----" lines is ignored.

        @param keyfile: contents of a PEM-encoded file that contains the private
            key.
        @return: a PrivateKey object
        '''

        der = rsa.pem.load_pem(keyfile, b('RSA PRIVATE KEY'))
        return cls._load_pkcs1_der(der)

    def _save_pkcs1_pem(self):
        '''Saves a PKCS#1 PEM-encoded private key file.

        @return: contents of a PEM-encoded file that contains the private key.
        '''

        der = self._save_pkcs1_der()
        return rsa.pem.save_pem(der, b('RSA PRIVATE KEY'))


__all__ = ['PublicKey', 'PrivateKey']

if __name__ == '__main__':
    import doctest
    
    try:
        for count in range(100):
            (failures, tests) = doctest.testmod()
            if failures:
                break

            if (count and count % 10 == 0) or count == 1:
                print('%i times' % count)
    except KeyboardInterrupt:
        print('Aborted')
    else:
        print('Doctests done')
