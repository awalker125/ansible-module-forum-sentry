 #!/usr/bin/python

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.forumsentry import forum_sentry_argument_spec
from ansible.module_utils.forumsentry import forum_sentry_required_together
from ansible.module_utils.forumsentry import AnsibleForumSentry

def main():

  module_args = dict(
    name                                = dict( type ='str'  ),
    aclPolicy                           = dict( type ='str'  ),
    description                         = dict( type ='str'  ),
    enabled                             = dict( type ='bool' ),
    errorTemplate                       = dict( type ='str'  ),
    ipAclPolicy                         = dict( type ='str'  ),
    listenerHost                        = dict( type ='str'  ),
    listenerSSLEnabled                  = dict( type ='bool' ),
    listenerSSLPolicy                   = dict( type ='str'  ),
    passwordAuthenticationRealm         = dict( type ='bool' ),
    passwordParameter                   = dict( type ='str'  ),
    port                                = dict( type ='int'  ),
    readTimeoutMillis                   = dict( type ='int'  ),
    requirePasswordAuthentication       = dict( type ='bool' ),
    useBasicAuthentication              = dict( type ='bool' ),
    useChunking                         = dict( type ='bool' ),
    useCookieAuthentication             = dict( type ='bool' ),
    useDeviceIp                         = dict( type ='bool' ),
    useDigestAuthentication             = dict( type ='bool' ),
    useFormPostAuthentication           = dict( type ='bool' ),
    useKerberosAuthentication           = dict( type ='bool' ),
    usernameParameter                   = dict( type ='str'  )
  )

  module_args.update(forum_sentry_argument_spec)

  sentry_required_if = [
    [ 'state' , 'present' , [ 'name' , 'port' ] ] ,
    [ 'state' , 'absent' , [ 'name' ] ]
  ]

  ssl_policy_required_together = [
    [ 'listenerSSLEnabled' , 'listenerSSLPolicy' ]
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
  
  service = '/restApi/v1.0/policies/httpListenerPolicies'

  if module.params['state'] == 'present':
    forum.createSentryObject( service )
  else:
    forum.deleteSentryObject( service , module.params['name'] )

  module.exit_json(**forum.result)

if __name__ == '__main__':
  main()
