# Project setup details

## Steps to create infrastructure for pipeline (from a windows perso

### GCP VM (+ SSH Access)

1. Create new project and set up billing in GCP console
2. [Create SSH Keys](https://cloud.google.com/compute/docs/connect/create-ssh-keys)
  - Make a new .ssh directory
  - Run command to create SSH keys in a file named, say, gcp
  - Enter public SSH key in GCP Compute Engine Metadata
  - Create a config file within .ssh directory with following contents
```
Host <VM alias>
	HostName <VM external IP>
	User <username-used-to-generate-keys>
	IdentityFile path/to/file/.ssh/gcp
```
3. Create new VM instance
  - Select region closest to your current location
  - Select machine type (recommended: e2-standard-2)
  - Change boot disk to Ubuntu 20.04 LTS with 20GB size
4. SSH into VM using ```ssh <VM alias>``` command
5. Install [Anaconda for Linux](https://www.anaconda.com/products/distribution) on VM
  - Use wget to download latest Anaconda version for Linux
  - Run the executable file with bash command
  - Log out and log back in using ```source .bashrc``` to complete installation
6. Install Docker (To Be Continued)
