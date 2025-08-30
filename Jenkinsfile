pipeline {
    agent any
    environment {
        // Opcional: variables globales, p. ej. nombre de la imagen Docker
        IMAGE_NAME = "ermesliriano/my-flask-app"
    }
    stages {
        stage('Checkout') {
            steps {
                // Jenkins ya realiza checkout automático si se usa Pipeline from SCM; si no, usar:
                git 'https://github.com/ermesliriano/my_flask_app.git'
            }
        }
        stage('Build Docker Image') {
            steps {
                script {
                    // Construir la imagen Docker con tag "latest"
                    dockerImage = docker.build("${IMAGE_NAME}:latest")
                }
            }
        }
        stage('Push Docker Image') {
            steps {
                script {
                    // Autenticarse en Docker Hub y pushear la imagen
                    docker.withRegistry('https://index.docker.io/v1/', 'dockerhub-creds') {
                        dockerImage.push()  // push de la etiqueta "latest"
                    }
                }
            }
        }
        stage('Deploy to EC2') {
            steps {
                // Usar la credencial SSH (key pair) para conectar al servidor de despliegue
                sshagent(['jenkins-keypair']) {
                    // Copiar el archivo deploy.yml al servidor remoto (por SSH)
                    sh 'scp -o StrictHostKeyChecking=no deploy.yml ec2-user@<IP_SERVIDOR_DEPLOY>:/home/ec2-user/deploy.yml'
                    // Ejecutar docker-compose en el servidor remoto para actualizar el despliegue
                    sh 'ssh -o StrictHostKeyChecking=no ec2-user@<IP_SERVIDOR_DEPLOY> "docker-compose -f /home/ec2-user/deploy.yml pull && docker-compose -f /home/ec2-user/deploy.yml up -d"'
                }
            }
        }
    }
}
