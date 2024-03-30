import os
import subprocess

def init_project(scope=globals(), cfg={}, **kwargs):
   
    import os
    if not os.path.exists('/kaggle/working/resyslab_utils'):
        print("\033[1;31m---------------you could have to clone resyslab_utils first!---------------\033[0m")
        return
    # init prj_rsa
    rsa_dir = os.path.expanduser('~/.ssh/')
    os.makedirs(rsa_dir, exist_ok=True)
    subprocess.run(["cp", "/kaggle/input/sgu24-prj-data/data/ssh/sguprj24_rsa", os.path.join(rsa_dir, "sguprj24_rsa")], check=True)
    subprocess.run(["chmod", "600", os.path.join(rsa_dir, "sguprj24_rsa")], check=True)

    # Configuring SSH for GitHub
    ssh_config = """
    Host github.com
        HostName ssh.github.com
        User git
        Port 443
        StrictHostKeyChecking no
        IdentityFile ~/.ssh/sguprj24_rsa
    """
    with open(os.path.join(rsa_dir, "config"), "w") as f:
        f.write(ssh_config)

    # pull prj repo
    branch = "dev"
    folder = "/kaggle/working/sgu24project"
    giturl = "git@github.com:dntai/sgu24prj.git"
    if not os.path.exists(folder):
        subprocess.run(["git", "clone", giturl, folder], check=True)
    else:
        subprocess.run(["git", "pull"], cwd=folder, check=True)
    subprocess.run(["git", "checkout", branch], cwd=folder, check=True)

    if scope is not None:
        scope.update(locals())

    # Call cloud_setup functions if needed
    # Example: cloud_setup.start_ssh(...)

    # Add any additional logic here

# Example usage:
init_project()
