# Update system
sudo apt update && sudo apt upgrade -y

# Install essential packages
sudo apt install git curl wget build-essential -y

# Update system
sudo apt update && sudo apt upgrade -y

# Install packages to allow apt to use a repository over HTTPS:
sudo apt install apt-transport-https ca-certificates software-properties-common -y

# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Add your user to docker group
sudo usermod -aG docker $USER

# Start Docker service
sudo service docker start

# Verify Docker installation
docker --version
docker-compose --version

# Install Python pip
sudo apt install python3-pip -y

cd ./interview/

# Build Docker containers 
docker compose build

# Start Docker containers in detached mode
docker compose up -d