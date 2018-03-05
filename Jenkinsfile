#!groovy
import groovy.json.JsonSlurperClassic
import static groovy.json.JsonOutput.*


@NonCPS
def parseJsonToMap(String json) {
    final slurper = new JsonSlurperClassic()
    return new HashMap<>(slurper.parseText(json))
}

def github(String event, Map data) {
    switch(event) {
    case "push":
        repo = data.repository
        sha = data.head_commit.id
        break

    case "pull_request":
        repo = data.pull_request.head.repo
        sha data.pull_request.head.sha
        break
    }
    sh """
    set -x
    git clone --quiet ${repo.clone_url}
    cd ${repo.name}
    git checkout -b ${sha} ${sha}
    git --no-pager log --pretty=medium -n1
    """
}

def comment(String event, Map data, String msg) {
    switch(event) {
        case "push":
            repo = data.repository.name
            user = data.repository.owner.login
            commit = data.head_commit.id
            break
        case "pull_request":
            repo = data.pull_request.head.repo.name
            commit = data.pull_request.head.sha
            user = data.pull_request.head.repo.user.login
            break
        default:
            println "Can't comment on ${event} events"
    }
    sh """ python <<EOF
from github import Github
g = Github('${env.GITHUB_ACCESS_TOKEN}')
user = g.get_user('${user}')
repo = user.get_repo('${repo}')
commit = repo.get_commit('${commit}')
commit.create_comment("${msg}")
        EOF
    """
}

pipeline {
    agent any
    options {
        timestamps()
    }
    parameters{
        string( name: 'sqs_body' )
        string( name: 'sqs_messageId' )
        string( name: 'sqs_bodyMD5' )
        string( name: 'sqs_receiptHandle' )
    }
    stages {
        stage('Setup'){
            steps{
                script {
                    def sqs_body = parseJsonToMap(params['sqs_body'])
                    if ('MessageAttributes' in sqs_body.keySet()){
                        msg_type = sqs_body.MessageAttributes['X-Github-Event'].Value
                        data = parseJsonToMap(sqs_body.Message)
                        print msg_type
                        println prettyPrint(toJson(data))
                    }
                    else { print sqs_body.keySet() }
                    comment(msg_type, data, "Testing started: ${env.BUILD_URL}")
                }
            }
        }
        stage('Test'){
            when { expression { msg_type in ['push', 'pull_request'] } }
            parallel{
                stage("Ansible latest"){
                    agent {
                        label 'manageiq-ansible-module:2.4'
                    }
                    environment {
                        TERM = 'xterm'
                        PREFIX="manageiq-ansible-${BUILD_NUMBER}-2.4-"
                        ANSIBLE_CONFIG = "test/ansible.cfg"
                    }
                    steps {
                        github(msg_type, data)
                        dir(data.repository.name){
                            sh "bundle install"
    // https://github.com/chef/kitchen-inspec/issues/119
    //                      sh "kitchen test --destroy always --concurrency"
                            sh """
                            kitchen create --concurrency
                            kitchen converge --concurrency | tee .kitchen/logs/converge.log
                            kitchen verify | tee .kitchen/logs/verify.log
                            kitchen destroy --concurrency
                            """
                            archiveArtifacts artifacts: '.kitchen/logs/*.log', fingerprint: true
                        }
                    }
                }
                stage("Ansible 2.4"){
                    agent {
                        label 'manageiq-ansible-module:2.4'
                    }
                    environment {
                        ANSIBLE_CONFIG = "test/ansible.cfg"
                    }
                    steps {
                        print "2.4"
                    }
                }
            }
        }
    }
    post{
        success {
           comment(msg_type, data, "Success: ${env.BUILD_URL} ")
        }
        failure {
           comment(msg_type, data, "Failed: ${env.BUILD_URL} ")
        }
    }
}
