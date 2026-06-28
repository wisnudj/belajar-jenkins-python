pipeline {
    agent any

    environment {
        IMAGE_NAME = "model-service-dummy"
        IMAGE_TAG  = "${env.BUILD_NUMBER}"
        CONTAINER_NAME = "model-service"
        MINIO_ACCESS   = credentials('minio-access-key')
        MINIO_SECRET   = credentials('minio-secret-key')
    }
    
    stages {
        stage("download model") {
            steps {
                sh "mc alias set myminio http://localhost:9000 ${MINIO_ACCESS} ${MINIO_SECRET}"
                sh "mc cp myminio/models/face_detection.json ./models"
            }
        }
        stage("build") {
            steps {
                sh "podman build -t ${IMAGE_NAME}:${IMAGE_TAG} ."
            }   
        }
        stage("deploy") {
            steps {
                sh "podman stop ${CONTAINER_NAME} || true"
                sh "podman rm ${CONTAINER_NAME} || true"
                sh "podman run -d --network=host --log-driver=k8s-file --name ${CONTAINER_NAME} ${IMAGE_NAME}:${IMAGE_TAG}"
            }
        }
    }
}