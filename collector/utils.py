from __future__ import absolute_import

import cv2


def clock():
    return cv2.getTickCount() / cv2.getTickFrequency()


class StatValue:
    def __init__(self, smooth_coef=0.5):
        self.value = None
        self.smooth_coef = smooth_coef

    def update(self, v):
        if self.value is None:
            self.value = v
        else:
            c = self.smooth_coef
            self.value = c * self.value + (1.0 - c) * v


class FrameHelper(object):

    @staticmethod
    def rescale_frame(frame, scale_percent=50):
        """
        Rescale a frame for the given scale percent.
        :param frame: The frame to rescale.
        :param scale_percent: The scale percent ratio to apply. Default is 50.
        :return: A new rescaled frame.
        """

        width = int(frame.shape[1] * scale_percent / 100)
        height = int(frame.shape[0] * scale_percent / 100)
        dim = (width, height)

        return cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)

    @staticmethod
    def resize_frame(frame, width=640, height=480):
        return cv2.resize(frame, (width, height))


class PubSubClient(object):
    def __init__(self, project='alert-shape-256811', topic='ml-flow'):
        from google.cloud import pubsub

        # Used for batching frames
        settings = pubsub.types.BatchSettings(
                max_messages=5,
                max_latency=1,
        )
        self.publisher = pubsub.PublisherClient(settings)
        self.topic_path = self.publisher.topic_path(project, topic)

    def publish(self, frame_as_bytes):
        future = self.publisher.publish(self.topic_path, data=frame_as_bytes)
        print('Published id: %s', future.result())