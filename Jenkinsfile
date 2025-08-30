pipeline {
    agent any 
    environment {
        // Variables de entorno para nombre y versión de imagen
        IMAGE_NAME = "ermesliriano/my-flask-app"
        IMAGE_TAG = "v${BUILD_NUMBER}"            // Ejemplo: usar el número de build como tag
        IMAGE = "${IMAGE_NAME}:${IMAGE_TAG}"
        // Credenciales para Docker Registry (configuradas en Jenkins Credentials)
        DOCKERHUB_CREDS = 'dockerhub-creds'
        // Datos de servidor de despliegue
        DEPLOY_HOST = "172.31.34.199"
        DEPLOY_USER = "ubuntu"  // usuario remoto con permisos Docker
    }
    stages {
        stage('Build Docker Image') {
            steps {
                echo "Construyendo imagen Docker: ${IMAGE}"
                // Construir la imagen Docker con el tag especificado
                sh 'docker build -t $IMAGE .'
            }
        }
        stage('Push to Registry') {
            steps {
                echo "Pusheando imagen ${IMAGE} al registro"
                // Login al registro Docker (por ejemplo Docker Hub)
                withCredentials([usernamePassword(credentialsId: "$DOCKERHUB_CREDS", 
                                                 usernameVariable: 'DOCKER_USER', 
                                                 passwordVariable: 'DOCKER_PASS')]) {
                    sh 'echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin'
                }
                // Enviar la imagen al registro
                sh 'docker push $IMAGE'
            }
        }
        stage('Deploy with Ansible') {
            steps {
                echo "Desplegando la aplicación con Ansible..."
                // Ejecutar el playbook Ansible pasando la imagen como extra-var
                // Usa inventario sencillo con la IP/host del servidor remoto
                sshagent(['ansible-ssh-credential-id']) {  // credencial SSH para Ansible
                    sh '''
                       ansible-playbook -i "${DEPLOY_HOST}," -u ${DEPLOY_USER} \
                       --private-key ~/.ssh/id_rsa \
                       deploy_app.yml -e "docker_image=${IMAGE}"
                       '''
                }
            }
        }
    }
    post {
        failure {
            echo "Deployment failed. Check logs and possibly rolled back to previous version."
        }
    }
}
