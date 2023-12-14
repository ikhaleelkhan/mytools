import os
import subprocess

def run_command(command):
    try:
        subprocess.check_call(command, shell=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        exit(1)

def main():
    # Update and upgrade system
    run_command("sudo apt-get -y update")
    run_command("sudo apt-get -y upgrade")

    # Install required packages
    packages = [
        "libcurl4-openssl-dev",
        "libssl-dev",
        "jq",
        "ruby-full",
        "libcurl4-openssl-dev libxml2 libxml2-dev libxslt1-dev ruby-dev build-essential libgmp-dev zlib1g-dev",
        "build-essential libssl-dev libffi-dev python-dev",
        "python-setuptools",
        "libldns-dev",
        "python3-pip",
        "python-pip",
        "python-dnspython",
        "git",
        "rename",
        "xargs",
        "awscli"
    ]

    for package in packages:
        run_command(f"sudo apt-get install -y {package}")

    # Clone and set up recon_profile
    run_command("git clone https://github.com/nahamsec/recon_profile.git")
    run_command("cat recon_profile/bash_profile >> ~/.bash_profile")
    run_command("source ~/.bash_profile")

    # Create a tools folder in the home directory
    run_command("mkdir ~/tools")
    run_command("cd ~/tools")

    # Install Golang if not installed
    if not os.environ.get("GOPATH"):
        print("It looks like go is not installed, would you like to install it now?")
        choice = input("Please select an option (yes/no): ")
        if choice.lower() == "yes":
            run_command("wget https://dl.google.com/go/go1.13.4.linux-amd64.tar.gz")
            run_command("sudo tar -xvf go1.13.4.linux-amd64.tar.gz")
            run_command("sudo mv go /usr/local")
            os.environ["GOROOT"] = "/usr/local/go"
            os.environ["GOPATH"] = "$HOME/go"
            os.environ["PATH"] = "$GOPATH/bin:$GOROOT/bin:$PATH"
            with open("~/.bash_profile", "a") as bash_profile:
                bash_profile.write("export GOROOT=/usr/local/go\n")
                bash_profile.write("export GOPATH=$HOME/go\n")
                bash_profile.write("export PATH=$GOPATH/bin:$GOROOT/bin:$PATH\n")
            run_command("source ~/.bash_profile")
        else:
            print("Please install go and rerun this script")
            print("Aborting installation...")
            exit(1)

    # Reminder to set up AWS credentials
    print("Don't forget to set up AWS credentials!")

    # Install Aquatone
    run_command("go get github.com/michenriksen/aquatone")

    # Install Chromium
    run_command("sudo snap install chromium")

    # Install JSParser
    run_command("git clone https://github.com/nahamsec/JSParser.git")
    run_command("cd JSParser*")
    run_command("sudo python setup.py install")
    run_command("cd ~/tools")

    # Install Sublist3r
    run_command("git clone https://github.com/aboul3la/Sublist3r.git")
    run_command("cd Sublist3r*")
    run_command("pip install -r requirements.txt")
    run_command("cd ~/tools")

    # Install other tools (add more here)

    print("Done! All tools are set up in ~/tools")
    run_command("ls -la")
    print("One last time: don't forget to set up AWS credentials in ~/.aws/!")

if __name__ == "__main__":
    main()
