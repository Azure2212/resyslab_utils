def connect_vscode(scope = globals(), cfg = {}, **kwargs):
    # kaggle config
    import base64
    from kaggle_secrets import UserSecretsClient
    user_secrets = UserSecretsClient()
    print(kwargs['folder'])
    print(kwargs['giturl'])
    %run /kaggle/working/resyslab_utils/resyslab_utils/clouds/cloud_setup.py
    kaggle_cfg = {}
    for name in ['NGROK_TOKEN_1', 'ID_RSA_PUB', 'SSH_PASS']:
        try:
            kaggle_cfg[name] = user_secrets.get_secret(name)
        except:
            pass    
    kaggle_cfg.update(**cfg)

    ngrok_token_val = kaggle_cfg.get("NGROK_TOKEN_1", "")
    id_rsa_pub      = kaggle_cfg.get("ID_RSA_PUB", "")
    ssh_pass_val    = kaggle_cfg.get("SSH_PASS", "12345")
    
    # ssh
    start_ssh(id_rsa_pub=id_rsa_pub,
              install_ssh=True, 
              config_ssh=True, 
              password=ssh_pass_val)
    
    # open port ssh to public
    start_ngrok([ngrok_token_val])