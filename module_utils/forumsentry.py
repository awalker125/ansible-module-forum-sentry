#!/usr/bin/python

from ansible.module_utils.basic import AnsibleModule

import requests
import json
import socket

forum_sentry_argument_spec = dict(
  sentryProtocol        = dict( type ='str',  default='http', choices=['http', 'https'] ),
  sentryHost            = dict( type ='str',  required=True ),
  sentryPort            = dict( type ='int',  default=80 ),
  sentryUsername        = dict( type ='str',  required=True ),
  sentryPassword        = dict( type ='str',  required=True ),
  state                 = dict( type ='str',  default='present', choices=['present', 'absent'] )
)

class AnsibleForumSentry( object ):


  def __init__( self , module ):
    self.module = module
    self.result = { 'changed': False }
    self.__url = self.module.params['sentryProtocol'] + "://" + self.module.params['sentryHost'] + ":" + str( self.module.params['sentryPort'] )
    self.__auth = auth=( self.module.params['sentryUsername'] , self.module.params['sentryPassword'] )


  def getCertificates( self, name ):

    service = '/restApi/v1.0/policies/x509Certificates'

    httpGet = requests.get( self.__url + service , auth=self.__auth , verify=True )

    if ( httpGet.status_code == 200 ):
      certs = json.loads( httpGet.text )
      certsList = []

      for cert in certs['policy']:
        if name in cert['name']:
          certsList.append( cert['name'] )

      return certsList
    else:
      self.module.fail_json( msg='Unable to get certificates: ' + str ( httpGet.status_code ) + ' - ' + httpGet.text )


  def getKeyPairs( self, name ):

    service = '/restApi/v1.0/policies/keyPairs'

    httpGet = requests.get( self.__url + service , auth=self.__auth , verify=True )

    if ( httpGet.status_code == 200 ):
      keyPairs = json.loads( httpGet.text )
      keyPairList = []

      for keyPair in keyPairs['policy']:
        if name in keyPair['name']:
          keyPairList.append( keyPair['name'] )

      return keyPairList
    else:
      self.module.fail_json( msg='Unable to get Key Pairs: ' + str ( httpGet.status_code ) + ' - ' + httpGet.text )


  def getSignerGroups( self , name ):

    service = '/restApi/v1.0/policies/signerGroups'

    httpGet = requests.get( self.__url + service , auth=self.__auth , verify=True )

    if ( httpGet.status_code == 200 ):
      signerGroups = json.loads( httpGet.text )
      signerGroupsList = []

      for signerGroup in signerGroups['policy']:
        if name in signerGroup['name']:
          signerGroupsList.append( signerGroup['name'] )

      return signerGroupsList
    else:
       self.module.fail_json( msg='Unable to get Signer Groups: ' + str ( httpGet.status_code ) + ' - ' + httpGet.text )


  def importFileX509OrPkcs7( self ):

    service = '/restApi/v1.0/policies/keyPairs/import/fileX509OrPkcs7'

    formValues={}

    for key in self.module.argument_spec:
      if ( key not in forum_sentry_argument_spec ) and ( key != 'certificateFile' ):
        formValues[key] = self.module.params[key]

    keyFile = open( self.module.params['certificateFile'], 'rb' )
    fileValues={ 'certificateFile' : keyFile }

    try:
      httpPost = requests.post( self.__url + service , auth=self.__auth , files=fileValues, data=formValues, verify=True )
      if ( httpPost.status_code == 202 ):
        self.result['changed'] = True
      elif ( httpPost.status_code == 409 ):
        self.result['changed'] = False
      else:
        self.module.fail_json( msg='Unable to import X509 or PKCS7: ' + str ( httpPost.status_code ) + ' - ' + httpPost.text )
    finally:
      keyFile.close()


  def importJksStore( self ):

    service = '/restApi/v1.0/policies/keyPairs/import/jksStore'

    formValues={}

    for key in self.module.argument_spec:
      if ( key not in forum_sentry_argument_spec ) and ( key != 'keyStoreFile' ):
        formValues[key] = self.module.params[key]

    keyFile = open( self.module.params['keyStoreFile'], 'rb' )
    fileValues={ 'keyStoreFile' : keyFile }

    try:
      httpPost = requests.post( self.__url + service , auth=self.__auth , files=fileValues, data=formValues, verify=True )
      if ( httpPost.status_code == 202 ):
        self.result['changed'] = True
      elif ( httpPost.status_code == 409 ):
        self.result['changed'] = False
      else:
        self.module.fail_json( msg='Unable to import X509 or PKCS7: ' + str ( httpPost.status_code ) + ' - ' + httpPost.text )
    finally:
      keyFile.close()


  def importLdapX509OrPkcs7( self ):

    service = '/restApi/v1.0/policies/keyPairs/import/ldapX509OrPkcs7'

    formValues={}

    for key in self.module.argument_spec:
      if ( key not in forum_sentry_argument_spec ):
        formValues[key] = self.module.params[key]

    httpPost = requests.post( self.__url + service , auth=self.__auth , data=formValues, verify=True )

    if ( httpPost.status_code == 202 ):
      self.result['changed'] = True
    elif ( httpPost.status_code == 409 ):
      self.result['changed'] = False
    else:
      self.module.fail_json( msg='Unable to import X509 or PKCS7: ' + str ( httpPost.status_code ) + ' - ' + httpPost.text )


  def importPkcs1OrPkcs8( self ):

    service = '/restApi/v1.0/policies/keyPairs/import/pkcs1OrPkcs8'

    formValues={}

    for key in self.module.argument_spec:
      if ( key not in forum_sentry_argument_spec ):
        if ( key != 'keyStoreFile' ) or ( key != 'certificateFile' ):
          formValues[key] = self.module.params[key]

    certificateFile = open( self.module.params['certificateFile'] , 'rb' )
    keyFile = open( self.module.params['keyFile'] , 'rb' )

    fileValues={ 'keyFile' : keyFile, 'certificateFile' : certificateFile }

    try:
      httpPost = requests.post( self.__url + service , auth=self.__auth , files=fileValues, data=formValues, verify=True )
      if ( httpPost.status_code == 202 ):
        self.result['changed'] = True
      elif ( httpPost.status_code == 409 ):
        self.result['changed'] = False
      else:
        self.module.fail_json( msg='Unable to import X509 or PKCS7: ' + str ( httpPost.status_code ) + ' - ' + httpPost.text )
    finally:
      certificateFile.close()
      keyFile.close()


  def importPkcs12( self ):
  
    service = '/restApi/v1.0/policies/keyPairs/import/pkcs12'
  
    formValues={}
	
    for key in self.module.argument_spec:
      if ( key not in forum_sentry_argument_spec ) and ( key != 'keyAndCertificateFile' ):
        formValues[key] = self.module.params[key]
    
    keyFile = open( self.module.params['keyAndCertificateFile'], 'rb' )
    fileValues={ 'keyAndCertificateFile' : keyFile }

    try:
      httpPost = requests.post( self.__url + service , auth=self.__auth , files=fileValues , data=formValues , verify=True )
      if ( httpPost.status_code == 202 ):
        self.result['changed'] = True
      elif ( httpPost.status_code == 409 ):
        self.result['changed'] = False
      else:
        self.module.fail_json( msg='Unable to import X509 or PKCS7: ' + str ( httpPost.status_code ) + ' - ' + httpPost.text )
    finally:
      keyFile.close()

    self.module.exit_json(**self.result)


  def deleteCertificate( self, name ):

    service = '/restApi/v1.0/policies/x509Certificates/'

    httpDelete = requests.delete( self.__url + service + name , auth=self.__auth , verify=True )

    if ( httpDelete.status_code == 200 ):
      self.result['changed'] = True
    elif ( httpDelete.status_code == 404 ):
      self.result['changed'] = False
    else:
      self.module.fail_json( msg='Unable to delete Certificate: ' + str ( httpDelete.status_code ) + ' - ' + httpDelete.text )


  def deleteKeyPair( self, name ):

    service = '/restApi/v1.0/policies/keyPairs/'

    httpDelete = requests.delete( self.__url + service + name , auth=self.__auth , verify=True )

    if ( httpDelete.status_code == 200 ):
      self.result['changed'] = True
    elif ( httpDelete.status_code == 404 ):
      self.result['changed'] = False
    else:
      self.module.fail_json( msg='Unable to delete Key Pair: ' + str ( httpDelete.status_code ) + ' - ' + httpDelete.text )


  def deleteSignerGroup( self , name ):

    service = '/restApi/v1.0/policies/signerGroups/'

    httpDelete = requests.delete( self.__url + service + name , auth=self.__auth , verify=True )

    if ( httpDelete.status_code == 200 ):
      self.result['changed'] = True
    elif ( httpDelete.status_code == 404 ):
      self.result['changed'] = False
    else:
      self.module.fail_json( msg='Unable to delete Signer Group: ' + str ( httpDelete.status_code ) + ' - ' + httpDelete.text )


  def deleteKeyPairPolicy( self ):
    
    signerGroups = self.getSignerGroups( self.module.params['name'] )

    if signerGroups:
      for signerGroup in signerGroups:
        self.deleteSignerGroup( signerGroup )

    certificates = self.getCertificates( self.module.params['name'] )

    if certificates:
      for certificate in certificates:
        self.deleteCertificate( certificate )

    keyPairs = self.getKeyPairs( self.module.params['name'] )

    if keyPairs:
      for keyPair in keyPairs:
        self.deleteKeyPair( keyPair )

    self.module.exit_json(**self.result)

