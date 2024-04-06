"""
cloud_setup
+ start_ssh

Modified: 2024/01/18
Created : 2024/01/18
(c) Tran Anh Tuan 
Mail: Dasanbob22122002@gmail.com
"""
import os
current_path = os.path.abspath(globals().get("__file__","."))
current_dir = os.path.dirname(current_path)

root_dir = os.path.abspath(f"{current_dir}/../../../")

def start_ssh(id_rsa_pub = "", password = "", install_ssh = False, config_ssh = False):
    """
    Start SSH as follows:
    + Add id_rsa.pub into ~/.ssh/authorized_keys
    + Install SSH service with Port 22 and password
    + Set command prompt

    Modified: 2024/01/18
    Created : 2024/01/18
    """    
    from IPython import get_ipython
    import os
    print(f'{"*" * 10} SETUP SSH SERVICE {"*"*10}')

    if install_ssh is True:
        get_ipython().system('echo "> Install ssh service..."')
        get_ipython().system('apt-get install ssh -y 2>&1 > /dev/null')
    
    if id_rsa_pub != "":
        get_ipython().system('echo "> Copy public key to authorized keys..."')
        get_ipython().system('mkdir -p ~/.ssh')
        get_ipython().system(f'echo {id_rsa_pub} > ~/.ssh/authorized_keys')

    if config_ssh is True:
        get_ipython().system('echo "> Config ssh service..."')
        get_ipython().system("sed -i 's/^#Port.*/Port 22/' /etc/ssh/sshd_config")
        get_ipython().system("sed -i 's/^PasswordAuthentication .*/PasswordAuthentication yes/' /etc/ssh/sshd_config")
        get_ipython().system("sed -i 's/^#Port.*/Port 22/' /etc/ssh/sshd_config")
        get_ipython().system("sed -i 's/^#ListenAddress 0.*/ListenAddress 0.0.0.0/' /etc/ssh/sshd_config")
        get_ipython().system("sed -i 's/^#ListenAddress ::.*/ListenAddress ::/' /etc/ssh/sshd_config")

        get_ipython().system("sed -i 's/^#PermitRootLogin.*/PermitRootLogin yes/' /etc/ssh/sshd_config")
        get_ipython().system("sed -i 's/^#PubkeyAuthentication.*/PubkeyAuthentication yes/' /etc/ssh/sshd_config")
        get_ipython().system("sed -i 's/^#PasswordAuthentication.*/PasswordAuthentication yes/' /etc/ssh/sshd_config")

        get_ipython().system("sed -i 's/^#AllowAgentForwarding.*/AllowAgentForwarding yes/' /etc/ssh/sshd_config")
        get_ipython().system("sed -i 's/^#AllowTcpForwarding.*/AllowTcpForwarding yes/' /etc/ssh/sshd_config")
        get_ipython().system("sed -i 's/^#PermitTTY.*/PermitTTY yes/' /etc/ssh/sshd_config")
        get_ipython().system("sed -i 's/^#GatewayPorts.*/GatewayPorts yes/' /etc/ssh/sshd_config")
        # !systemctl reload sshd

    if password != "":
        get_ipython().system('echo "> Set root password..."')
        get_ipython().system(f'echo -e "$password\n{password}" | passwd root >/dev/null 2>&1')

    get_ipython().system('echo "> Restart SSH service..."')
    get_ipython().system('service ssh restart')
    print(f"")

    get_ipython().system('echo "> Process ~/.bashrc to registry PS1, TERM..."')
    get_ipython().system('grep -qx "^PS1=.*$" ~/.bashrc || echo "PS1=" >> ~/.bashrc')
    dest = "PS1='\\[\\e]0;\\u@\h: \\w\\a\\]${debian_chroot:+($debian_chroot)}\\[\\033[01;32m\\]\\u@\\h\\[\\033[00m\\]:\\[\\033[01;34m\\]\\w\\[\\033[00m\\]\$ '"
    cmd = "sed -i \"s/$(echo $src | sed -e 's/\\([[\\/.*]\\|\\]\\)/\\\\&/g').*/$(echo $dest | sed -e 's/[\\/&]/\\\\&/g')/g\" ~/.bashrc"
    get_ipython().system(f'src="PS1=" && echo $src && dest="{dest}" && echo "$dest" && {cmd}')

    cmd = 'grep -qx "^TERM=.*$" ~/.bashrc || echo "TERM=xterm-256color" >> ~/.bashrc'
    get_ipython().system(f'{cmd}')
    print(f"")
    
    print(f'{"-" * 10} Finished {"-"*10}\n')
    pass # start_ssh

def start_ngrok(ngrok_tokens = [], 
                ngrok_binds  = {
                    'ssh': {'port':22, 'type':'tcp'}, 
                    'vscode': {'port':9000, 'type':'http'}
                }
               ):
    """
    start_ngrok:
    + ngrok_tokens: list of token getting from Authtoken in dashboard at https://ngrok.com
    + ngrok_binds : default: 
        {
            'ssh'   : {'port':22, 'type':'tcp'}, 
            'vscode': {'port':9000, 'type':'http'}
        }
    """
    def default_handler(ngrok, ngrok_info = {}):
        # bind with code-server: port 9000
        # vscode_tunnel = ngrok.connect(9000, "http")
        
        # bind with ports
        for name in ngrok_binds:
            try:
                tunnel = ngrok.connect(ngrok_binds[name].get('port', 80), 
                                   ngrok_binds[name].get('type', 'tcp'))
                ngrok_info[name] = tunnel
            except:
                print('failt')
            pass
        pass # default_handler
    
    print(f'{"*" * 10} SETUP NGROK {"*"*10}')
    try:
        from pyngrok import ngrok, conf
    except:
        # install pyngrok
        print(f'> Install ngrok...')
        get_ipython().system('pip install -qqq pyngrok 2>&1 > /dev/null')
        from pyngrok import ngrok, conf

    print(f'> Kill ngrok process...')
    get_ipython().system('kill -9 "$(pgrep ngrok)"')
    
    print(f'> Binding ports...')
    list_regions = ["us", "en", "au", "vn"]
    url, ssh_tunnel = None, None
    is_success = False
    ngrok_info = {}
    for auth_token in ngrok_tokens:
        if is_success: break
        for region in list_regions:  
            try:
                conf.get_default().region = region
                ngrok.set_auth_token(auth_token)

                default_handler(ngrok, ngrok_info)

                print("> Registry success!")
                is_success = True
                break
            except Exception as e:
                print(e)
                pass    
        # for

    for key in ngrok_info:
        print(f'{key}: {ngrok_info[key]}')
    
    print(f"")
    print(f'{"-" * 10} Finished {"-"*10}\n')
    pass # start_ngrok
                
def setup_github_config(id_rsa_path):
    from IPython import get_ipython
    
    print("> Setup ssh github...")
    
    key_name = os.path.basename(id_rsa_path)
    key_path = f'~/.ssh/{key_name}'
    print(f"Key name: {key_name}")
    
    get_ipython().system("mkdir -p ~/.ssh")
    
    print(f'Copy: {id_rsa_path} --> {key_path}')
    get_ipython().system(f"cp '{id_rsa_path}' ~/.ssh/{key_name}")
    get_ipython().system(f"chmod 600 {key_path}")
    print("setup github_config finished")

    ssh_config_path = os.path.expanduser('~/.ssh/config')
    ssh_config_content = f"""
    Host github.com
        HostName ssh.github.com
        User git
        Port 443
        StrictHostKeyChecking no
        IdentityFile ~/.ssh/{key_name}
    """
    with open(ssh_config_path, 'w') as f:
        f.write(ssh_config_content)

    pass # setup_github_config

def connect_vscode(scope = globals(), cfg = {}, **kwargs):
    # kaggle config
    import base64
    from kaggle_secrets import UserSecretsClient
    user_secrets = UserSecretsClient()
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


def clone_project_from_github(scope=globals(), cfg={}, **kwargs):
    import os
    from IPython import get_ipython
    if not os.path.exists(f'{root_dir}/resyslab_utils'):
        print("\033[1;31m---------------you could have cloned resyslab_utils first!---------------\033[0m")
        return
    # init prj_rsa

    if('giturl' not in kwargs or 'folder' not in kwargs):
        print("\033[1;31m---------------you could have chose giturl or folder to clone first!---------------\033[0m")
        return

    if not os.path.exists(kwargs['folder']):
        if('branch' not in kwargs or kwargs['branch'] == ""):
            get_ipython().system(f"git clone {kwargs['giturl']} {kwargs['folder']}")     
        else:
            get_ipython().system(f"git clone --branch {kwargs['branch']} {kwargs['giturl']} {kwargs['folder']}")  
    else:
        get_ipython().system(f"!git pull {kwargs['folder']}")  
        
    if scope is not None:
        scope.update(locals())

    # Call cloud_setup functions if needed
    # Example: cloud_setup.start_ssh(...)

    # Add any additional logic here

# Example usage: