pipeline {
    agent any

    stages {
        stage('git scm update') {
            steps {
                git url: 'https://github.com/austin-kho/hRebs', branch: "dev"
            }
        }

        stage('docker build and push') {
            steps {
                sh '''
                docker build -t dokube/nginx:latest ./deploy/docker/nginx
                docker push dokube/nginx:latest
                docker build -t dokube/web:latest ./deploy/docker/python
                docker push dokube/web:latest
                '''
            }
        }

        stage('deploy kubernetes by helm') {
            steps {
                sh '''
                kubectl apply -f ./deploy/kubectl/ns-prod.yaml
                helm upgrade rebs ./deploy/helm --install -f ./deploy/helm/values-prod.yaml -n hrebs-prod
                '''
            }
        }

        stage('yarn build') {
            steps {
                sh '''
                cd ./app/vue3 && yarn && yarn build
                '''
            }
        }
    }
}
