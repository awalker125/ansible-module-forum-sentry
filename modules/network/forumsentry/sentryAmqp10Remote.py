 #!/usr/bin/python

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.forumsentry import forum_sentry_argument_spec
from ansible.module_utils.forumsentry import forum_sentry_required_together
from ansible.module_utils.forumsentry import AnsibleForumSentry

def main():

  module_args = dict(
    name 			= dict( type ='str' ),
    remoteServer 		= dict( type ='str' ),
    remotePort 			= dict( type ='int' ),
    enabled 			= dict( type ='bool'	, default = True ),
    idleTimeoutMillis 		= dict( type ='int'	, default = 30 ),
    transferTimeoutMillis 	= dict( type ='int'	, default = 30 ),
    credentialSource 		= dict( type ='str' 	, default = 'STATIC' , choices = ['STATIC' , 'DYNAMIC' , 'PROPAGATE'] ),
    userPolicy 			= dict( type ='str'	, default = '' ),
    useSsl 			= dict( type ='bool'	, default = False ),
    sslPolicy 			= dict( type ='str'	, default = '' ),
    saslMechanism 		= dict( type ='str' 	, default = 'NONE' , choices = ['NONE' , 'ANONYMOUS' , 'PLAIN' , 'CRAM_MD5' , 'EXTERNAL'] ),
    description 		= dict( type ='str'	, default = '' ),
    processResponse 		= dict( type ='bool'	, default = False ),
  )

  module_args.update( forum_sentry_argument_spec )

  sentry_required_if = [
    [ 'state' , 'present' , [ 'name' , 'remoteServer' , 'remotePort' ] ] ,
    [ 'state' , 'absent' , [ 'name' ] ]
  ]

  ssl_policy_required_together = [
    [ 'useSsl' , 'sslPolicy' ]
  ]

  module = AnsibleModule(
    argument_spec=module_args,
    supports_check_mode=True,
    required_if=sentry_required_if,
    required_together=forum_sentry_required_together + ssl_policy_required_together
  )

  forum = AnsibleForumSentry( module )

  if module.check_mode:
    return result
  
  service = '/restApi/v1.0/policies/amqp10RemotePolicies'

  if module.params['state'] == 'present':
    forum.createSentryObject( service )
  else:
    forum.deleteSentryObject( service , module.params['name'] )

  module.exit_json(**forum.result)

if __name__ == '__main__':
  main()
