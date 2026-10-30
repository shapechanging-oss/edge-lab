pipeline {
  agent {
    kubernetes {
      defaultContainer 'python'
      yaml '''
        apiVersion: v1
        kind: Pod
        spec:
          containers:
          - name: python
            image: python:3.12-slim
            command: [sleep]
            args: [infinity]
            env:
            - { name: PGHOST, value: localhost }
            - { name: PGUSER, value: postgres }
            - { name: PGPASSWORD, value: ci }
          - name: postgres                      # the equivalent of an Actions "service container"
            image: postgres:16
            env:
            - { name: POSTGRES_PASSWORD, value: ci }
          - name: shellcheck
            image: koalaman/shellcheck-alpine:stable
            command: [sleep]
            args: [infinity]
          - name: buildah
            image: quay.io/buildah/stable
            command: [sleep]
            args: [infinity]
            securityContext: { privileged: true }
      '''
    }
  }

  options {
    timeout(time: 30, unit: 'MINUTES')
    disableConcurrentBuilds(abortPrevious: true)
    buildDiscarder(logRotator(numToKeepStr: '50'))
  }

  environment {
    REGISTRY = 'ghcr.io/shapechanging-oss/edge-lab'
    IMAGE    = "${REGISTRY}:${env.GIT_COMMIT}"
  }

  stages {
    stage('Lint') {
      parallel {
        stage('shellcheck') {
          steps { container('shellcheck') { sh 'shellcheck scripts/*.sh' } }
        }
        stage('ruff') {
          steps { sh 'pip install -q ruff && ruff check app' }
        }
      }
    }

    stage('Test') {
      steps {
        container('postgres') {
          sh '''
            until pg_isready -U postgres; do sleep 1; done
            for pass in 1 2; do
              for f in migrations/*.sql; do psql -U postgres -v ON_ERROR_STOP=1 -f "$f"; done
            done
          '''
        }
        dir('app') {
          sh 'pip install -q -r requirements-dev.txt && pytest -q --junitxml=reports/junit.xml'
        }
      }
    }

    stage('Build and push') {
      when { branch 'main' }
      steps {
        container('buildah') {
          withCredentials([usernamePassword(credentialsId: 'ghcr',
                           usernameVariable: 'REG_USER', passwordVariable: 'REG_PASS')]) {
            sh '''
              echo "$REG_PASS" | buildah login -u "$REG_USER" --password-stdin ghcr.io
              buildah bud -t "$IMAGE" app
              buildah push --digestfile digest.txt "$IMAGE"
            '''
          }
        }
      }
    }

    stage('Deploy staging') {
      when { branch 'main' }
      steps { sh './scripts/deploy.sh staging "$REGISTRY@$(cat digest.txt)"' }
    }

    stage('Deploy production') {
      when { branch 'main' }
      input { message 'Deploy this build to production?'; ok 'Deploy' }
      steps { sh './scripts/deploy.sh production "$REGISTRY@$(cat digest.txt)"' }
    }
  }

  post {
    always  { junit allowEmptyResults: true, testResults: 'app/reports/*.xml' }
    failure { echo "Build failed: ${env.BUILD_URL}" }
  }
}
