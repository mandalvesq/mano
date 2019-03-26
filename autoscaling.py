import os
import boto3


class AutoScaling:
    def __init__(self, tag, name=None, min_size=None, max_size=None, desired_capacity=None, instances=None):
        self.tag = tag
        self.client = boto3.client('autoscaling',aws_access_key_id=os.getenv('aws_access_key_id'),
                                aws_secret_access_key=os.getenv('aws_secret_access_key'),
                                region_name='sa-east-1')
        """ :type : pyboto3.autoscaling """
        if self.tag == "":
            self.name = name
            self.min_size = min_size
            self.max_size = max_size
            self.desired_capacity = desired_capacity
            self.instances = instances
        else:
            self.__from_tag()

    def __from_tag(self):
        paginator = self.client.get_paginator('describe_auto_scaling_groups')
        page_iterator = paginator.paginate(
          PaginationConfig={'PageSize': 100}
        )

        filtered_asgs = page_iterator.search(
          'AutoScalingGroups[] | [?contains(Tags[?Key==`{}`].Value, `{}`)]'.format(
            'App', self.tag)
        )

        # for asg in filtered_asgs:
        #   asgs.append(asg['AutoScalingGroupName'])

        asg = list(filtered_asgs)[0]
        self.name = asg['AutoScalingGroupName']
        self.min_size = asg['MinSize']
        self.max_size = asg['MaxSize']
        self.desired_capacity = asg['DesiredCapacity']
        self.instances = asg['Instances']

    def turn_on(self, size=1):
        self.__change_autoscaling_size(size)

    def turn_off(self):
        self.__change_autoscaling_size(0)

    def __change_autoscaling_size(self, count):
        self.client.update_auto_scaling_group(
            AutoScalingGroupName=self.name,
            MinSize=count,
            MaxSize=count,
            DesiredCapacity=count,
        )

class Limits:
    def __init__(self):
        self.client = boto3.client('autoscaling',aws_access_key_id=os.getenv('aws_access_key_id'),
                                aws_secret_access_key=os.getenv('aws_secret_access_key'),
                                region_name='sa-east-1')
    def list_limits(self):
        self.describe_account_limits()
