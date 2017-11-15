 #!/usr/bin/python

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.forumsentry import forum_sentry_argument_spec
from ansible.module_utils.forumsentry import AnsibleForumSentry

def main():

  module_args = dict(
    name                                = dict(type ='str',  required=True),
    aclPolicy                           = dict(type ='str',  default=''),
    description                         = dict(type ='str',  default=''),
    enabled                             = dict(type ='bool', default=True),
    errorTemplate                       = dict(type ='str',  default=''),
    ipAclPolicy                         = dict(type ='str',  default=''),
    listenerHost                        = dict(type ='str',  default=''),
    listenerSSLEnabled                  = dict(type ='bool', default=False),
    listenerSSLPolicy                   = dict(type ='str',  default=''),
    passwordAuthenticationRealm         = dict(type ='bool', default=False),
    passwordParameter                   = dict(type ='str',  default=''),
    port                                = dict(type ='int',  default=8080),
    readTimeoutMillis                   = dict(type ='int',  default=0),
    requirePasswordAuthentication       = dict(type ='bool', default=False),
    useBasicAuthentication              = dict(type ='bool', default=False),
    useChunking                         = dict(type ='bool', default=True),
    useCookieAuthentication             = dict(type ='bool', default=False),
    useDeviceIp                         = dict(type ='bool', default=True),
    useDigestAuthentication             = dict(type ='bool', default=False),
    useFormPostAuthentication           = dict(type ='bool', default=False),
    useKerberosAuthentication           = dict(type ='bool', default=False),
    usernameParameter                   = dict(type ='str',  default='')
  )

  module_args.update(forum_sentry_argument_spec)

  module = AnsibleModule(
    argument_spec=module_args,
    supports_check_mode=True
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