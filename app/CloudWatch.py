import boto3
from datetime import datetime, timedelta
import app.config
import random
from pytz import timezone

class CloudWatch:

    @staticmethod
    def getEC2CPUUsageByID(id):
        '''
        get all ec2 instance from AWS
        :return: ec2 instances list. type ec2.instancesCollection
        '''
        metric_name = 'CPUUtilization'

        ##    CPUUtilization, NetworkIn, NetworkOut, NetworkPacketsIn,
        #    NetworkPacketsOut, DiskWriteBytes, DiskReadBytes, DiskWriteOps,
        #    DiskReadOps, CPUCreditBalance, CPUCreditUsage, StatusCheckFailed,
        #    StatusCheckFailed_Instance, StatusCheckFailed_System

        namespace = 'AWS/EC2'
        statistic = 'Average'  # could be Sum,Maximum,Minimum,SampleCount,Average
        client = boto3.client('cloudwatch')
        cpu = client.get_metric_statistics(
            Period=1 * 60,
            StartTime=datetime.utcnow() - timedelta(seconds=60 * 60),
            EndTime=datetime.utcnow() - timedelta(seconds=0 * 60),
            MetricName=metric_name,
            Namespace=namespace,  # Unit='Percent',
            Statistics=[statistic],
            Dimensions=[{'Name': 'InstanceId', 'Value': id}]
        )

        return cpu

    @staticmethod
    def putHttpRequestRateByID():
        client = boto3.client('cloudwatch',region_name='us-east-1')
        value = 1
        response = client.put_metric_data(
            Namespace='OpsNameSpace',
            MetricData=[
                {
                    'MetricName': 'HttpRequestCount',
                    'Dimensions': [
                        {
                            'Name': 'instanceID',
                            'Value': app.config.instanceID
                        },
                    ],
                    'Timestamp': datetime.now(timezone('Canada/Eastern')),
                    'Value': value,
                    'Unit': 'None',
                    'StorageResolution': 1
                },
            ]
        )

