from argparse import ArgumentParser
import os, subprocess 
parser = ArgumentParser()
parser.add_argument('--private-key-path',default="",type=str,help="private ssh path key for authority")

args = parser.parse_args()
private_key_name = args.private_key_path.split("/")[-1]

ssh_config_path = os.path.expanduser('~/.ssh/config')
ssh_config_content = f"""
    Host github.com
        HostName ssh.github.com
        User git
        Port 443
        StrictHostKeyChecking no
        IdentityFile ~/.ssh/{private_key_name}
    """


# List the files in the specified directory
subprocess.run(['ls',  args.private_key_path])

# Copy sguprj24_rsa file to the ~/.ssh directory
subprocess.run(['cp',  args.private_key_path, f'~/.ssh/{private_key_name}'])

# Change the permission of sguprj24_rsa file to 600
subprocess.run(['chmod', '600', f'~/.ssh/{private_key_name}'])

# List the files in the ~/.ssh directory
subprocess.run(['ls', '~/.ssh'])

with open(ssh_config_path, 'w') as f:
    f.write(ssh_config_content)
print("print successful!")