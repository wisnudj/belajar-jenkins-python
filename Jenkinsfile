pipeline {
    agent any

    environment {
        IMAGE_NAME = "model-service-dummy"
        IMAGE_TAG  = "v1"
        CONTAINER_NAME = "model-service"
        MINIO_ACCESS   = credentials('minio-access-key')
        MINIO_SECRET   = credentials('minio-secret-key')
    }

    parameters {
        persistentString(name: "ENVIRONMENT", defaultValue: "dev", description: "")
        persistentString(name: "MINIO_BUCKET", defaultValue: "dev-model-ml", description: "")
        persistentString(name: "BLOCKED_FIELD", defaultValue: "", description: "")
        persistentString(name: "COMPLETENESS", defaultValue: "", description: "")
        persistentString(name: "FACE_QUALITY", defaultValue: "", description: "")
        persistentString(name: "GLARE", defaultValue: "", description: "")
        persistentString(name: "OVERLAY_DETECTION", defaultValue: "", description: "")
        persistentString(name: "PRINTED_COPY", defaultValue: "", description: "")
    }
    
    stages {
        stage("download model") {
            steps {
                sh "mc alias set myminio http://172.17.0.3:9000 ${MINIO_ACCESS} ${MINIO_SECRET}"

                script {
                    def modelParams = [
                        BLOCKED_FIELD     : params.BLOCKED_FIELD,
                        COMPLETENESS      : params.COMPLETENESS,
                        FACE_QUALITY      : params.FACE_QUALITY,
                        GLARE             : params.GLARE,
                        OVERLAY_DETECTION : params.OVERLAY_DETECTION,
                        PRINTED_COPY      : params.PRINTED_COPY
                    ]

                    modelParams.each { name, value -> 
                        if (value?.trim()) {
                            echo "Downloading model for ${name}: ${value}"
                            sh "mc cp myminio/models/${value} ./models"
                        }
                    }
                }
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