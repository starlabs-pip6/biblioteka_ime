pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                echo 'Recent Updates Checked'
            }
        }
        stage('Install requirements') {
            steps {
                sh 'pip install -r requirements.txt'
                sh 'python3 manage.py makemigrations libri_im'
                sh 'python3 manage.py migrate'
                sh 'python3 manage.py loaddata Booksdata.json'
            }
        }
        stage('Deploy') {
            steps {
                sh 'systemctl restart nginx'
            }
        }
    }
}
