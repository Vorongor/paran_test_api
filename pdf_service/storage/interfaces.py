from abc import ABC, abstractmethod


class S3StorageInterface(ABC):

    @abstractmethod
    async def upload_file(self, file_name: str, file_data: bytes | bytearray) -> None:
        """
        Uploads a file to the storage.

        :param file_name: The name of the file to be stored.
        :param file_data: The file data in bytes.
        :return: URL of the uploaded file.
        """
        pass

    @abstractmethod
    async def get_file_url(self, file_name: str) -> str:
        """
        Generate a public URL for a file stored in the S3-compatible storage.

        :param file_name: The name of the file stored in the bucket.
        :return: The full URL to access the file.
        """
        pass


class SQSStorageInterface(ABC):

    @abstractmethod
    async def send_message(self, data: dict) -> None:
        """
        Sends a message to the queue.

        :param data: The data to be sent.
        """
        pass

    @abstractmethod
    async def receive_messages(self, max_msg: int = 1) -> dict:
        """
        Receive a message from a queue.

        :param max_msg:  The maximum number of messages to be received.

        :return: Response from the queue.
        """
        pass

    @abstractmethod
    async def delete_message(self, handler: str) -> None:
        """
        Deletes a message after processing it.

        :param handler:  The handler to be deleted.
        """
        pass
