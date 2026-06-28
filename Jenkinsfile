pipeline {
    agent any

    environment {
        IMAGE_NAME = "model-service-dummy"
        IMAGE_TAG  = "${env.BUILD_NUMBER}"
        CONTAINER_NAME = "model-service"
    }
    
    stages {
        stage("build") {
            steps {
                sh "podman build -t ${IMAGE_NAME}:${IMAGE_TAG} ."
            }   
        }
        stage("deploy") {
            steps {
                sh "podman stop ${CONTAINER_NAME} || true"
                sh "podman rm ${CONTAINER_NAME} || true"
                sh "podman run -dit 10080:10080 --name ${CONTAINER_NAME} ${IMAGE_NAME}:${IMAGE_TAG}"
            }
        }
    }
}