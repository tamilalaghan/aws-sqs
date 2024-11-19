import boto3,time

queue_name  = "BackgroundCheckApp"


sqs_client = boto3.client("sqs")

#print(sqs_client.list_queues())

def send_message(queueName,messageBody):
    
    print("Trying to send Message")
    try:
        sqs_client.send_message(
        QueueUrl = queueName,
        MessageBody =  messageBody)
        time.sleep(8)
        print("Message sent Success")
    
    except Exception as e:
        print(f"Exception raised {e}")
        


def receive_message(queueName,maxNumberMsg,waitTimeSec):
    
    try:
        print("Trying to fetch messages")
        message_info = sqs_client.receive_message(
            QueueUrl = queueName,
            MaxNumberOfMessages = maxNumberMsg,
            WaitTimeSeconds = waitTimeSec)
          
        
        if 'Messages' in message_info:
            print("Message Received")
            message_read = message_info['Messages'][0]['Body']
            receipt_handle = message_info['Messages'][0]['ReceiptHandle']
            print(f" Message : {message_read} \nReceiptHandle : {receipt_handle}")
            print("*********Delete Initiated*********")
            delete_message(queueName,receipt_handle)
        else:
            print("*************Waiting for Messages**************")
            time.sleep(5)
    
    except Exception as e:
        print(f"Exception raised {e}")
        
    

def delete_message(queueName,receiptHandle):
    try:
        print(f"Trying to delete the message {receiptHandle}")
        sqs_client.delete_message(
            QueueUrl =  queueName,
            ReceiptHandle = receiptHandle)
        time.sleep(3)
        print("Message deleted")
    except Exception as e:
        print(f"Exception raised {e}")
        


if __name__ == "__main__":
    send_message(queue_name,"This is First Sample Message")
    receive_message(queue_name,1,6)
   
    
    