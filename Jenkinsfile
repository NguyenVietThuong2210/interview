pipeline {
    agent any

    options {
        timestamps()
        disableConcurrentBuilds()
        ansiColor('xterm')
    }

    environment {
        COMPOSE_PROJECT_NAME = "interview"
        DOCKER_BUILDKIT = "1"
    }

    stages {

        stage('Checkout Source') {
            steps {
                checkout scm
            }
        }

        stage('Validate Environment') {
            steps {
                sh '''
                    docker --version
                    docker compose version
                '''
            }
        }

        stage('Build Docker Images') {
            steps {
                sh '''
                    docker compose build
                '''
            }
        }

        stage('Deploy Services') {
            steps {
                sh '''
                    docker compose up -d --build
                '''
            }
        }

        stage('Post-Deploy Health Check') {
            steps {
                sh '''
                    sleep 10
                    docker compose ps
                '''
            }
        }
    }

    post {
        success {
            echo "✅ Deployment succeeded"
        }

        failure {
            echo "❌ Deployment failed"
        }

        always {
            sh '''
                docker image prune -f
            '''
        }
    }
}