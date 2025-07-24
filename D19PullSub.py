from google.cloud import pubsub_v1

PROJECT_ID = "tranquil-post-461304-m7"
SUBSCRIPTION_ID = "errorsubs"  # replace with your actual subscription name

subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path(PROJECT_ID, SUBSCRIPTION_ID)

def callback(message):
    print(f"\n📨 Received message: {message.data.decode('utf-8')}")
    message.ack()  # Acknowledge receipt

# Listen for messages with a streaming pull
streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
print(f"Listening for messages on {subscription_path}...")

try:
    streaming_pull_future.result(timeout=60)  # Wait up to 30 seconds
except Exception as e:
    streaming_pull_future.cancel()
    print(f"Stopped listening: {e}")