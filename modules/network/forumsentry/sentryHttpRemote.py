 #!/usr/bin/python

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.forumsentry import forum_sentry_argument_spec
from ansible.module_utils.forumsentry import forum_sentry_required_together
from ansible.module_utils.forumsentry import AnsibleForumSentry

def main():

  module_args = dict(
    name                                = dict( type = 'str'  ),
    remoteServer			= dict( type = 'str'  ), 
    remotePort				= dict( type = 'int'  ),
    enabled				= dict( type = 'bool' ),
    useBasicAuth 			= dict( type = 'bool' ),
    proxyPolicy 			= dict( type = 'str'  ),
    SSLInitiationPolicy 		= dict( type = 'str'  ),
    tcpConnectionTimeout 		= dict( type = 'int'  ),
    httpAuthenticationUserPolicy 	= dict( type = 'str'  ),
    useChunking 			= dict( type = 'bool' ),
    tcpReadTimeout 			= dict( type = 'int'  ),
    enableSSL 				= dict( type = 'bool' ),
    remoteAuthentication 		= dict( type = 'str' , default = 'NONE' , choices = ['NONE' , 'STATIC' , 'DYNAMIC' , 'PROPAGATE'] ),
    processResponse 			= dict( type = 'bool'  )
  )

  module_args.update(forum_sentry_argument_spec)

  sentry_required_if = [
    [ 'state' , 'present' , [ 'name' , 'remoteServer' , 'remotePort' ] ] ,
    [ 'state' , 'absent' , [ 'name' ] ]
  ]

  ssl_sentry_required_together = [
    [ 'enableSSL' , 'SSLInitiationPolicy' ]
  ]

  module = AnsibleModule(
    argument_spec=module_args,
    supports_check_mode=True,
    required_if=sentry_required_if,
    required_together=forum_sentry_required_together + ssl_sentry_required_together
  )

  forum = AnsibleForumSentry( module )

  if module.check_mode:
    return result
  
  service = '/restApi/v1.0/policies/httpRemotePolicies'

  if module.params['state'] == 'present':
    forum.createSentryObject( service )
  else:
    forum.deleteSentryObject( service , module.params['name'] )

  module.exit_json(**forum.result)

if __name__ == '__main__':
  main()
