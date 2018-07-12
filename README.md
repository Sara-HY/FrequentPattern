###Frequent Pattern Mining on DBLP

**Data**:  All paper information of IJCAI, AAAI, COLT, CVPR, NIPS, KR, SIGIR, SIGKDD  in the DBLP database since 2007.

#####Task1: Find out the researchers for each conference respectively, and figure out who is still active or not based on publication time. 

Suppose authors who have published papers for the past three years (2015, 2016, 2017).

#####Task2: Based on the number of papers published by researchers collaborate with each other, find the 'team' of three or more people by frequent pattern mining .

Set the minimum support to 5, that is they have collaborated at least 5 papers together, and use the FP-growth algorithm for frequent pattern mining.

#####Task3: Each paper will cover one or more topics. Set the keywords first, and then extract the most frequently topics of each team based on their papers.

Use the LDA model for topic mining and set the topic number to 10.

#####Task4: Teams and topics will change over time.  Describe the changes of the composition of the teams and their research topics according to the time period (five, three, two or one year).

Filter the teams publishing papers in three different years at least, and find the topic changes on every publication.