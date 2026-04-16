from abc import ABC, abstractmethod
from typing import Any

# Allowed standard library imports: abc, collections, typing


class DataProcessor(ABC):

    def __init__(self) -> None:
        self.queue: list = list()
        self.counter: int = 0

    @abstractmethod
    def validate(self, data: Any) -> bool:
        pass

    @abstractmethod
    def ingest(self, data: Any) -> None:
        pass

    def output(self) -> tuple[int, str]:
        if self.queue:
            return self.queue.pop(0)
        print("Data stream is empty.")

        return -1, ""


class NumericProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        if isinstance(data, (int, float)):
            return True

        if isinstance(data, list) and all(
            isinstance(i, (int, float)) for i in data
        ):
            return True
        return False

    def ingest(self, data: int | float | list[int] | list[float]) -> None:
        try:
            if self.validate(data):
                if isinstance(data, (int, float)):
                    self.queue.append((self.counter, str(data)))
                    self.counter += 1
                elif isinstance(data, list):
                    for item in data:
                        self.queue.append((self.counter, str(item)))
                        self.counter += 1
            else:
                raise ValueError("Improper numeric data")
        except ValueError as e:
            print(f"Got exception: {e}")


class TextProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        if isinstance(data, str):
            return True
        if isinstance(data, list) and all(isinstance(i, str) for i in data):
            return True
        return False

    def ingest(self, data: str | list[str]) -> None:
        try:
            if self.validate(data):
                if isinstance(data, str):
                    self.queue.append((self.counter, str(data)))
                    self.counter += 1
                elif isinstance(data, list):
                    for item in data:
                        self.queue.append((self.counter, str(item)))
                        self.counter += 1
            else:
                raise ValueError("Improper text data")
        except ValueError as e:
            print(f"Got exception: {e}")


class LogProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        if isinstance(data, dict):
            if all(
                isinstance(key, str) and isinstance(value, str)
                for key, value in data.items()
            ):
                return True
        elif isinstance(data, list):
            return all(
                isinstance(i, dict)
                and all(
                    isinstance(key, str) and isinstance(value, str)
                    for key, value in i.items()
                )
                for i in data
            )

        return False

    def ingest(self, data: dict[str, str] | list[dict[str, str]]) -> None:
        try:
            if self.validate(data):
                if isinstance(data, dict):
                    for key, value in data.items():
                        self.queue.append(
                            (
                                self.counter,
                                f"\
{str(key)}: {str(value)}",
                            )
                        )
                        self.counter += 1
                elif isinstance(data, list):
                    for i in data:
                        log_level = i.get("log_level")
                        log_message = i.get("log_message")

                        self.queue.append(
                            (
                                self.counter,
                                f"\
{log_level}: {log_message}",
                            )
                        )

                        self.counter += 1

            else:
                raise ValueError(f"Invalid data: {data}. \
The key, value in dict must be string.")
        except ValueError as e:
            print(f"Got exception: {e}")


class DataStream:
    def __init__(self) -> None:
        self.processors: list[DataProcessor] = []

    def register_processor(self, proc: DataProcessor) -> None:
        self.processors.append(proc)

    def process_stream(self, stream: list[Any]) -> None:
        for data in stream:
            handle = False
            try:
                for proc in self.processors:
                    if proc.validate(data):
                        proc.ingest(data)
                        handle = True

                if not handle:
                    raise ValueError(
                        f"Can't process element in stream: {data}"
                    )

            except ValueError as e:
                print(f"DataStream error - {e}")

    def print_statistics(self, name: str, obj: DataProcessor) -> None:
        print(f"{name} total {obj.counter} items \
processed, remaining {len(obj.queue)}\
on processor")


# def print_processors_stats(self) -> None:


if __name__ == "__main__":
    dataStream = DataStream()
    print("=== Code Nexus - Data Stream ===\n")
    print("Initialize Data Stream...")
    print("== DataStream statistics ==")
    print("No processor found, no data\n")
    print("Registering Numeric Processor\n")
    numericProcessor = NumericProcessor()
    data = [
        "Hello world",
        [3.14, -1, 2.71],
        [
            {
                "log_level": "WARNING",
                "log_message": "Telnet access!Use ssh instead",
            },
            {"log_level": "INFO", "log_message": "User wil is connected"},
        ],
        42,
        ["Hi", "five"],
    ]
    print(f"Send first batch of data on stream: {data}")
    dataStream.register_processor(numericProcessor)
    dataStream.process_stream(data)
    print("== DataStream statistics ==")
    dataStream.print_statistics("Numeric Processor: ", numericProcessor)
    print()
    print("Registering other data processors\n")
    textProcessor = TextProcessor()
    logProcessor = LogProcessor()
    print("Send the same batch again")
    print("== DataStream statistics ==")
    dataStream.register_processor(textProcessor)
    dataStream.register_processor(logProcessor)
    dataStream.process_stream(data)

    dataStream.print_statistics("Numeric Processor: ", numericProcessor)
    dataStream.print_statistics("Text Processor ", textProcessor)
    dataStream.print_statistics("Log Processor: ", logProcessor)
    print("\nConsume some elements from the data \
processors: Numeric 3, Text 2, Log 1")
    numericProcessor.output()
    numericProcessor.output()
    numericProcessor.output()
    textProcessor.output()
    textProcessor.output()
    logProcessor.output()
    print("== DataStream statistics ==")
    dataStream.print_statistics("Numeric Processor: ", numericProcessor)
    dataStream.print_statistics("Text Processor ", textProcessor)
    dataStream.print_statistics("Log Processor: ", logProcessor)
