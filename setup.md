# Project setup details

## Steps to create infrastructure for pipeline (from a windows perso

### GCP VM (+ SSH Access)

1. Create new project and set up billing in GCP console
2. Create new service account in GCP console
  - Include the following roles (pre-defined GCP roles for simplicity, not desirable for production)
    - Viewer
    - Storage Admin (Google Cloud Storage access)
    - Storage Object Admin (access to objects withing Cloud Storage)
    - BigQuery Admin (database access)
3. [Create SSH Keys](https://cloud.google.com/compute/docs/connect/create-ssh-keys)
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
4. Create new VM instance
  - Select region closest to your current location
  - Select machine type (recommended: e2-standard-2)
  - Change boot disk to Ubuntu 20.04 LTS with 20GB size
5. SSH into VM using ```ssh <VM alias>``` command
6. Install [Anaconda for Linux](https://www.anaconda.com/products/distribution) on VM
  - Use wget to download latest Anaconda version for Linux
  - Run the executable file with bash command
  - Log out and log back in using ```source .bashrc``` to complete installation
7. Install Docker on VM
  - Use ```sudo apt-get install docker.io``` command to install docker. ```sudo apt-get update``` might be required first
  - Follow [this](https://github.com/sindresorhus/guides/blob/main/docker-without-sudo.md) link to be able to use docker without sudo
  - Test installation using ```docker``` command
8. Clone this GitHub repo using ```git clone https://github.com/falakjain98/twitter_analytics_pipeline.git``` and ```cd``` into repo
9. Install docker-compose
  - Use [this](https://github.com/docker/compose/releases) for the latest version of docker-compose for linux
  - Create new bin folder using ```mkdir bin``` and ```cd``` into  it
  - Download the executable file using ```wget <executable-link> -O docker-compose```
  - Convert the file to executable mode ```chmod +x docker-compose```
  - Check installation ```./docker-compose```
  - Add file to path variable with ```nano .bashrc``` and enter the following information at the end of the file
```
export PATH="${HOME}/bin:${PATH}"
```
  - ```source .bashrc``` to log out and log in for installation completion
10. Connect to VM from VS Code using Remote - SSH extension (offered by Microsoft) and forward port 8080 to local
11. Install terraform for Linux using [this link](https://developer.hashicorp.com/terraform/downloads)
  - Download the executable file with ```wget <executable-link>``` in the bin folder
  - Unzip download zip file ```unzip <filename>``` (```sudo apt-get install unzip``` may be required first). Remove zip file if not required
  - Test installation ```terraform -version```
12. Save GCP IAM credentials to VM
  - Save credentials in .json format to local as google-credentials.json
  - ```sftp <VM alias>``` into VM and navigate to .gc folder
  - ```put google-credentials.json``` to transfer credentials file to VM folder
  - Set `GOOGLE_APPLICATION_CREDENTIALS` to point to this file
```
export GOOGLE_APPLICATION_CREDENTIALS=~/.gc/google-credentials.json
```
  - Authenticate credentials with Google CLI
```
gcloud auth activate-service-account --key-file $GOOGLE_APPLICATION_CREDENTIALS
```
  - `terraform init`, `terraform plan`, `terraform apply` and `terraform destroy` should perform IaC functions from the terraform folder in the github repo now
