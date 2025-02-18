
# Creating a HDInsight Hadoop cluster

1. Use Azure portal to create a new HDInsight resource
2. Connect to the cluster using SSH: 'ssh sshuser@hadoopimc-ssh.azurehdinsight.net'
3. Take a look at the available examples: 'yarn jar /usr/hdp/current/hadoop-mapreduce-client/hadoop-mapreduce-examples.jar'
4. Let's take a look at the wordcount example: 'yarn jar /usr/hdp/current/hadoop-mapreduce-client/hadoop-mapreduce-examples.jar wordcount'
5. Let's try it out with some data: 'yarn jar /usr/hdp/current/hadoop-mapreduce-client/hadoop-mapreduce-examples.jar wordcount /example/data/gutenberg/davinci.txt /example/data/davinciwordcount'
6. Now we take a look at the output: 'hdfs dfs -cat /example/data/davinciwordcount/*'
7. We are not submitting our own code to the cluster, using the provided mapper.py and reduced.py files (warning Python 2.7)
8. We upload both files to the cluster: 'scp mapper.py reducer.py sshuser@hadoopimc-ssh.azurehdinsight.net:'
9. Connect again with the cluster using SSH
10. Start the new job: 'hadoop jar /usr/hdp/current/hadoop-mapreduce-client/hadoop-streaming.jar -files mapper.py,reducer.py -mapper mapper.py -reducer reducer.py -input /example/data/gutenberg/davinci.txt -output /example/data/davinciwordcount'
11. Take a look at the results: 'hdfs dfs -cat /example/data/davinciwordcount3/*'