from confluent_kafka import Producer, KafkaException
import logging
from fastapi import Request

logger = logging.getLogger(__name__)


def get_kafka(request:Request):
    return request.app.state.kafka


class KafkaService:
    def __init__(self, *bootstrap_servers:str):
        self.__producer = Producer({'bootstrap.servers':",".join(bootstrap_servers), #bootstrap_servers,
                                    "enable.idempotence": "true", #no duplicates on retry
                                    "acks": "all", #wait for all replicas to ack
                                    "linger.ms": 5, #wait for 5ms before sending
                                    "compression.type": "lz4"
                                    })
    def _delivery_status(self, err, msg):
            if err is not None:
                logger.error('Message delivery failed for %s: %s', msg.key(), err)
            else:
                logger.info('Message delivered to %s [%d] @ %d', msg.topic(), msg.partition(), msg.offset())

    def produce_message(self, topic: str, key: str, value: bytes) -> None:
        try:
            self.__producer.produce(topic, key=key, value=value, callback=self._delivery_status)

        except BufferError:
            self.__producer.poll(1) # drain, then retry once
            self.__producer.produce(topic, key=key, value=value, callback=self._delivery_status)

        except KafkaException:
            logger.exception("produce_message error: %s", topic)
            raise
        self.__producer.poll(0) # server delivery callbacks, non-blocking

    def close(self) -> None:
        self.__producer.flush(10) # wait up to 10s
    