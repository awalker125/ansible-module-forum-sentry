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


  def createSentryObject( self , service ):

    jsonMessage={}

    for key in self.module.argument_spec:
      if key not in forum_sentry_argument_spec:
        jsonMessage[key] = self.module.params[key]

    message = json.dumps( jsonMessage )

    httpPost = requests.post( self.__url + service , auth=self.__auth , data=message, verify=True , headers={ 'Content-Type': 'application/json' } )   

    if ( httpPost.status_code == 201 ):
      self.result['changed'] = True
    elif ( httpPost.status_code == 409 ):
      self.result['changed'] = False
    else:
      self.module.fail_json( msg='Unable to create ' + name + ': ' + str( httpPost.status_code ) + ' - ' + httpPost.text )
 
  
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


  def importSentryObject( self , service , keys='' ):
    
    file = ''
    fileValues = {}        
    formValues = {}

    for key in self.module.argument_spec:
      if ( key not in forum_sentry_argument_spec ) and ( key not in keys ):
        formValues[key] = self.module.params[key]
      
    # Some nasty ass code up in here... fix it!
    for key in keys.split(','):
      file = open( self.module.params[key] , 'rb' )
      fileValues[key] = file
      
    try:
      if fileValues:
        httpPost = requests.post( self.__url + service , auth=self.__auth , files=fileValues , data=formValues , verify=True )
      else:
        httpPost = requests.post( self.__url + service , auth=self.__auth , data=formValues , verify=True )
 
      if ( httpPost.status_code == 202 ):
        self.result['changed'] = True
      elif ( httpPost.status_code == 409 ):
        self.result['changed'] = False
      else:
        self.module.fail_json( msg='Unable to import ' + service.rsplit('/', 1)[-1] + ': ' + str( httpPost.status_code ) + ' - ' + httpPost.text )

    finally:
      file.close()

