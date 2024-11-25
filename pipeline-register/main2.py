import time
import random
import os

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
        print(f"Processing {data} at {self.name}...")
        time.sleep(1)  # Simulasi waktu proses
        self.output = data * 2  # Operasi sederhana
        return self.output

# Pipeline dan visualisasi
class Pipeline:
    def __init__(self):
        self.stages = []

    def add_stage(self, stage):
        self.stages.append(stage)

    def execute(self, data):
        results = []
        print("\nStarting pipeline...\n")
        for i, stage in enumerate(self.stages):
            self.visualize(i, data)
            output = stage.process(data)
            results.append(output)
            data = output
        self.visualize(len(self.stages), None)  # Final state
        return results

    def visualize(self, current_stage, data):
        os.system('cls' if os.name == 'nt' else 'clear')  # Clear terminal
        print("Pipeline Visualization:")
        for i, stage in enumerate(self.stages):
            if i == current_stage:
                print(f"  -> {stage.name}: [PROCESSING: {data}]")
            else:
                print(f"  -> {stage.name}: [IDLE]")
        time.sleep(0.5)

# Program utama
if __name__ == "__main__":
    # Membuat register
    reg1 = Register("Register 1")

    # Memuat nilai ke register
    reg1.load(random.randint(1, 10))

    # Membuat pipeline
    pipeline = Pipeline()
    pipeline.add_stage(PipelineStage("Stage 1"))
    pipeline.add_stage(PipelineStage("Stage 2"))
    pipeline.add_stage(PipelineStage("Stage 3"))

    # Eksekusi pipeline dengan input dari register
    if reg1.value is not None:
        results = pipeline.execute(reg1.value)
        print("\nPipeline Execution Complete.")
        print(f"Final Results: {results}")

    # Clear register
    reg1.clear()
