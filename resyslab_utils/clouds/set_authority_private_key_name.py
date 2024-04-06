from argparse import ArgumentParser
import os, subprocess 
parser = ArgumentParser()
parser.add_argument('--private-key-path',default="",type=str,help="private ssh path key for authority")

args = parser.parse_args()
private_key_name = args.private_key_path.split("/")[-1]
print(args.private_key_path)

subprocess.run(['cd', '/kaggle/working'], shell=True)

ssh_config_path = os.path.expanduser('~/.ssh/config')

directory = os.path.expanduser(f'~/.ssh{private_key_name}')  # This will expand '~' to the user's home directory

os.makedirs(directory, exist_ok=True)

subprocess.run(['ls',  args.private_key_path])

subprocess.run(['cp',  args.private_key_path, f'~/.ssh/{private_key_name}'])

subprocess.run(['chmod', '600', f'~/.ssh/{private_key_name}'])

subprocess.run(['ls', '~/.ssh'])


ssh_config_content = f"""
    Host github.com
       PreferredAuthentications publickey
       StrictHostKeyChecking no
       IdentityFile ~/.ssh/{private_key_name}
    """
with open(ssh_config_path, 'w') as f:
    f.write(ssh_config_content)

print("print successful!")