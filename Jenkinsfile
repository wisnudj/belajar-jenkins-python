pipeline {
    agent any

    environment {
        IMAGE_NAME = "model-service-dummy:1.0.0"
    }
    
    stages {
        stage("build") {
            steps {
                sh "podman build -t ${IMAGE_NAME} ."
            }   
        }
    }
}