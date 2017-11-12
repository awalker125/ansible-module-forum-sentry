#!/usr/bin/python

from ansible.module_utils.basic import AnsibleModule

import requests
import json

forum_sentry_argument_spec = dict(
  sentryProtocol        = dict( type ='str', default='http', choices=['http', 'https'] ),
  sentryHost            = dict( type ='str' ),
  sentryPort            = dict( type ='int' ),
  sentryUsername        = dict( type ='str' ),
  sentryPassword        = dict( type ='str' ),
  state                 = dict( type ='str',  default='present', choices=['present', 'absent'] )
)

forum_sentry_required_together = [
  [ 'sentryHost' , 'sentryPort' , 'sentryUsername' , 'sentryPassword' ]
]

class AnsibleForumSentry( object ):



  def __init__( self , module ):
    self.module = module
    self.result = { 'changed' : False }
    self.__url = self.module.params['sentryProtocol'] + "://" + self.module.params['sentryHost'] + ":" + str( self.module.params['sentryPort'] )
    self.__auth = auth=( self.module.params['sentryUsername'] , self.module.params['sentryPassword'] )



  def createSentryObject( self , service , data , files={} , isJson=False):    

    if files:
      httpPost = requests.post( self.__url + service , auth=self.__auth , files=files, data=data, verify=True )
    else:
      if isJson:
        httpPost = requests.post( self.__url + service , auth=self.__auth , data=data, verify=True , headers={ 'Content-Type': 'application/json' } )
      else:
        httpPost = requests.post( self.__url + service , auth=self.__auth , data=data, verify=True )

    if ( httpPost.status_code == 202 ):
      self.result['changed'] = True
    elif ( httpPost.status_code == 409 ):
      self.result['changed'] = False
    else:
      self.module.fail_json( msg='Unable to import ' + service.rsplit('/', 1)[-1] + ': ' + str( httpPost.status_code ) + ' - ' + httpPost.text )


  
  def deleteSentryObject( self , service , name ):
  
    httpDelete = requests.delete( self.__url + service + '/' + name , auth=self.__auth , verify=True )

    if ( httpDelete.status_code == 200 ):
      self.result['changed'] = True
    elif ( httpDelete.status_code == 404 ):
      self.result['changed'] = False
    else:
      self.module.fail_json( msg='Unable to delete ' + service.rsplit('/', 1)[-1] + ': ' + str( httpDelete.status_code ) + ' - ' + httpDelete.text )
    


  def getSentryObject( self , service , name ):
    
    httpGet = requests.get( self.__url + service , auth=self.__auth , verify=True )

    if ( httpGet.status_code == 200 ):
      items = json.loads( httpGet.text )
      itemsList = []

      for item in items['policy']:
        if name in item['name']:
          itemsList.append( item['name'] )

      return itemsList
    else:
      self.module.fail_json( msg='Unable to get ' + service.rsplit('/', 1)[-1] + ': ' + str( httpGet.status_code ) + ' - ' + httpGet.text )



  def importFileX509OrPkcs7( self ):

    formValues={}

    for key in self.module.argument_spec:
      if ( key not in forum_sentry_argument_spec ) and ( key != 'certificateFile' ):
        formValues[key] = self.module.params[key]

    keyFile = open( self.module.params['certificateFile'], 'rb' )
    fileValues={ 'certificateFile' : keyFile }

    try:
      self.createSentryObject( '/restApi/v1.0/policies/keyPairs/import/fileX509OrPkcs7' , formValues , fileValues )
    finally:
      keyFile.close()



  def importJksStore( self ):

    formValues={}

    for key in self.module.argument_spec:
      if ( key not in forum_sentry_argument_spec ) and ( key != 'keyStoreFile' ):
        formValues[key] = self.module.params[key]

    keyFile = open( self.module.params['keyStoreFile'], 'rb' )
    fileValues={ 'keyStoreFile' : keyFile }

    try:
      self.self.createSentryObject( '/restApi/v1.0/policies/keyPairs/import/jksStore' , formValues , fileValues )
    finally:
      keyFile.close()



  def importLdapX509OrPkcs7( self ):

    formValues={}

    for key in self.module.argument_spec:
      if ( key not in forum_sentry_argument_spec ):
        formValues[key] = self.module.params[key]

    self.createSentryObject( '/restApi/v1.0/policies/keyPairs/import/ldapX509OrPkcs7' , formValues )



  def importPkcs1OrPkcs8( self ):

    formValues={}

    for key in self.module.argument_spec:
      if ( key not in forum_sentry_argument_spec ):
        if ( key != 'keyStoreFile' ) or ( key != 'certificateFile' ):
          formValues[key] = self.module.params[key]

    certificateFile = open( self.module.params['certificateFile'] , 'rb' )
    keyFile = open( self.module.params['keyFile'] , 'rb' )

    fileValues={ 'keyFile' : keyFile, 'certificateFile' : certificateFile }

    try:
       self.createSentryObject( '/restApi/v1.0/policies/keyPairs/import/pkcs1OrPkcs8' , formValues , fileValues )
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
      self.createSentryObject( '/restApi/v1.0/policies/keyPairs/import/pkcs12' , formValues , fileValues )
    finally:
      keyFile.close()

    
