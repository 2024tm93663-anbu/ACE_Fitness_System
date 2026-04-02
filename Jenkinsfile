pipeline {
    agent any

    stages {

        stage('Check Python') {
            steps {
                bat "C:\\Users\\Vasanth\\AppData\\Local\\Programs\\Python\\Python311\\python.exe --version"
            }
        }

        stage('Install Dependencies') {
            steps {
                bat "C:\\Users\\Vasanth\\AppData\\Local\\Programs\\Python\\Python311\\python.exe -m pip install -r requirements.txt"
            }
        }

        stage('Run App') {
            steps {
                bat "C:\\Users\\Vasanth\\AppData\\Local\\Programs\\Python\\Python311\\python.exe app.py"
            }
        }

    }

    post {
        success {
            echo 'Pipeline succeeded!'
        }
        failure {
            echo 'Pipeline failed!'
        }
    }
}