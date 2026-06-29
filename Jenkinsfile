pipeline {
    agent any

    environment {
        IMAGE_NAME = "model-service-dummy"
        IMAGE_TAG  = "${env.BUILD_NUMBER}"
        CONTAINER_NAME = "model-service"
        MINIO_ACCESS   = credentials('minio-access-key')
        MINIO_SECRET   = credentials('minio-secret-key')
    }

    triggers {
        GenericTrigger(
            causeString: 'Triggered by MinIO',
            token: '11d8dc20a6a417d9fdc98f7a4c43992741',
            printContributedVariables: true,
            printPostContent: true
        )
    }
    
    stages {
        stage("download model") {
            steps {
                sh "mc alias set myminio http://172.17.0.3:9000 ${MINIO_ACCESS} ${MINIO_SECRET}"
                sh "mc cp myminio/models/face_detection.json ./models"
            }
        }
        stage("build") {
            steps {
                sh "docker build -t ${IMAGE_NAME}:${IMAGE_TAG} ."
            }   
        }
        stage("deploy") {
            steps {
                sh "docker stop ${CONTAINER_NAME} || true"
                sh "docker rm ${CONTAINER_NAME} || true"
                sh "docker run -d --network=host --name ${CONTAINER_NAME} ${IMAGE_NAME}:${IMAGE_TAG}"
            }
        }
    }
}