pipeline {
    agent any
    options {
        disableConcurrentBuilds()
        buildDiscarder(logRotator(daysToKeepStr: '31', artifactNumToKeepStr: '5'))
    }
    parameters {
        string(name: 'last_time', defaultValue: '', description: '前回集計期間のログが置いてあるディレクトリのパスを入力する。')
        string(name: 'this_time', defaultValue: '', description: '今回集計期間のログが置いてあるディレクトリのパスを入力する。')
        choice choices: ['2019', '2020', '2021'], description: '今回集計期間の年を入力する。', name: 'year'
        choice choices: ['6', '9', '12', '3'], description: '今回集計期間の月を入力する。', name: 'month'
    }
    stages {
        stage('build'){
            steps {
                sh 'chmod 744 ./ShopRanking.py'
                sh 'python ./ShopRanking.py $last_time $this_time $year $month'
            }
        }
    }
    post {
        cleanup {
            deleteDir()
        }
    }
}
