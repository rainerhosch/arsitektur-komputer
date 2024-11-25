import matplotlib.pyplot as plt
import time
import random

# Simulasi register
class Register:
    def __init__(self, name):
        self.name = name
        self.value = None

    def load(self, value):
        self.value = value
        print(f"{self.name} loaded with value {value}")

    def clear(self):
        print(f"{self.name} cleared")
        self.value = None

# Simulasi pipeline stage
class PipelineStage:
    def __init__(self, name):
        self.name = name
        self.input = None
        self.output = None

    def process(self, data):
        print(f"Processing {data} at {self.name}")
        time.sleep(0.5)  # Simulasi waktu proses
        self.output = data * 2  # Operasi sederhana
        print(f"{self.name} output: {self.output}")

# Pipeline dan register
class Pipeline:
    def __init__(self):
        self.stages = []

    def add_stage(self, stage):
        self.stages.append(stage)

    def execute(self, data):
        print("Starting pipeline...")
        for stage in self.stages:
            stage.process(data)
            data = stage.output

# Visualisasi pipeline
class PipelineVisualizer:
    def __init__(self, pipeline):
        self.pipeline = pipeline

    def visualize(self, data):
        values = []
        labels = [stage.name for stage in self.pipeline.stages]

        for stage in self.pipeline.stages:
            stage.process(data)
            values.append(stage.output)
            data = stage.output

        # Plot data
        plt.figure(figsize=(10, 6))
        plt.bar(labels, values, color='skyblue')
        plt.title('Pipeline Processing Visualization')
        plt.xlabel('Pipeline Stages')
        plt.ylabel('Output Values')
        plt.show()

# Simulasi program utama
if __name__ == "__main__":
    # Membuat register
    reg1 = Register("Register 1")
    reg2 = Register("Register 2")

    # Memuat nilai ke register
    reg1.load(random.randint(1, 10))

    # Membuat pipeline
    pipeline = Pipeline()
    pipeline.add_stage(PipelineStage("Stage 1"))
    pipeline.add_stage(PipelineStage("Stage 2"))
    pipeline.add_stage(PipelineStage("Stage 3"))

    # Eksekusi pipeline dengan input dari register
    if reg1.value is not None:
        pipeline.execute(reg1.value)

    # Visualisasi pipeline
    visualizer = PipelineVisualizer(pipeline)
    visualizer.visualize(reg1.value)

    # Clear register
    reg1.clear()
