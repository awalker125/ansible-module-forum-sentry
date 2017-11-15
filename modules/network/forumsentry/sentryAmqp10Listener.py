 #!/usr/bin/python

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.forumsentry import forum_sentry_argument_spec
from ansible.module_utils.forumsentry import forum_sentry_required_together
from ansible.module_utils.forumsentry import AnsibleForumSentry

def main():

  module_args = dict(
    name 		= dict( type ='str' ),
    ip 			= dict( type ='str' ),
    port 		= dict( type ='int'	, default=5672 ),
    useDeviceIp 	= dict( type ='bool'	, default=True ),
    enabled 		= dict( type ='bool'	, default=True ),
    aclPolicy 		= dict( type ='str'	, default='' ),
    ipAclPolicy 	= dict( type ='str'	, default='' ),
    readTimeoutMillis 	= dict( type ='int'	, default = 30 ),
    saslMechanism 	= dict( type ='str' 	, default = 'NONE' , choices = ['NONE' , 'ANONYMOUS' , 'PLAIN' , 'CRAM_MD5' , 'EXTERNAL'] ),
    useSsl 		= dict( type ='bool'	, default=False ),
    sslPolicy 		= dict( type ='str'     , default=False ),
    description 	= dict( type ='str'	, default='' ),
    interface 		= dict( type ='str' 	, default = 'WAN' , choices = [ 'WAN' , 'LAN' ] ),
    errorTemplate 	= dict( type ='str'	, default='' )
  )

  module_args.update(forum_sentry_argument_spec)

  sentry_required_if = [
    [ 'state' , 'present' , [ 'name' , 'ip' , 'port' ] ] ,
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
  
  service = '/restApi/v1.0/policies/amqp10ListenerPolicies'

  if module.params['state'] == 'present':
    forum.createSentryObject( service )
  else:
    forum.deleteSentryObject( service , module.params['name'] )

  module.exit_json(**forum.result)

if __name__ == '__main__':
  main()
