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
        persistentString(name: "ENVIRONMENT", defaultValue: "development", description: "")
        persistentString(name: "MINIO_BUCKET", defaultValue: "dev-model-ml", description: "")
        persistentString(name: "BLOCKED_FIELD", defaultValue: "default/blocked_field_mobilenetv2.onnx", description: "")
        persistentString(name: "COMPLETENESS", defaultValue: "default/completeness_mobilenetv2.onnx", description: "")
        persistentString(name: "FACE_QUALITY", defaultValue: "default/face_quality_mobilenetv2.onnx", description: "")
        persistentString(name: "GLARE", defaultValue: "default/glare_mobilenetv2.onnx", description: "")
        persistentString(name: "OVERLAY_DETECTION", defaultValue: "default/overlay_detection_mobilenetv2.onnx", description: "")
        persistentString(name: "PRINTED_COPY", defaultValue: "default/printed_copy_mobilenetv2.onnx", description: "")
    }
    
    stages {
        stage("download model") {
            steps {
                sh "mc alias set myminio http://172.17.0.3:9000 ${MINIO_ACCESS} ${MINIO_SECRET}"

                script {
                    echo "environment is ${params.ENVIRONMENT}"
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
                            sh "mc cp myminio/${MINIO_BUCKET}/${value} ./models"
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
