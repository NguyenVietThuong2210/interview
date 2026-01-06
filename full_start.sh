# Update system
sudo apt update && sudo apt upgrade -y

# Install essential packages
sudo apt install git curl wget build-essential -y

# Update system
sudo apt update && sudo apt upgrade -y

# Install packages to allow apt to use a repository over HTTPS:
sudo apt install apt-transport-https ca-certificates software-properties-common gnupg -y

# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo apt install docker-compose

# Add your user to docker group
sudo usermod -aG docker $USER

# Start Docker service
sudo service docker start

# Verify Docker installation
docker --version
docker-compose --version

sudo apt update && sudo apt upgrade -y

# install Java (OpenJDK 17) for Jenkins
sudo apt install -y openjdk-17-jdk
sudo update-alternatives --config java
sudo systemctl daemon-reexec

sudo apt update && sudo apt upgrade -y

# Jenkins setup on Ubuntu (host machine)
curl -fsSL https://pkg.jenkins.io/debian-stable/jenkins.io-2023.key | sudo tee /usr/share/keyrings/jenkins-keyring.asc > /dev/null
echo "deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc] https://pkg.jenkins.io/debian-stable binary/" | sudo tee /etc/apt/sources.list.d/jenkins.list > /dev/null

sudo apt update && sudo apt upgrade -y
sudo apt install -y jenkins
sudo systemctl enable jenkins
sudo systemctl start jenkins

# Get admin: sudo cat /var/lib/jenkins/secrets/initialAdminPassword

# Install Python pip
sudo apt install python3-pip -y

git clone https://github.com/NguyenVietThuong2210/interview.git
cd ./interview/interview

chmod +x ./scripts/entrypoint.sh

# Build Docker containers 
docker compose build

# Start Docker containers in detached mode
docker compose up -d

# Run Django migrations
# docker exec -it productionmanagebe-web-1 python manage.py migrate
# docker exec -it productionmanagebe-web-1 python manage.py createsuperuser
