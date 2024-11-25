import time
import os
import random

# Simulasi pipeline stage
class PipelineStage:
    def __init__(self, name):
        self.name = name
        self.input = None
        self.output = None

    def process(self, data):
        time.sleep(1)  # Simulasi waktu proses
        self.output = data * 2  # Operasi sederhana
        return self.output

# Pipeline dengan visualisasi terminal
class Pipeline:
    def __init__(self):
        self.stages = []

    def add_stage(self, stage):
        self.stages.append(stage)

    def execute(self, data):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Starting pipeline...\n")
        for current_stage, stage in enumerate(self.stages):
            self.visualize(current_stage, data)
            data = stage.process(data)
        self.visualize(len(self.stages), None)  # Final state
        print(f"\nPipeline complete. Final output: {data}\n")
        return data

    def visualize(self, current_stage, data):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Pipeline Visualization:")
        for i, stage in enumerate(self.stages):
            if i < current_stage:
                print(f"  {stage.name}: [COMPLETED: {stage.output}]")
            elif i == current_stage:
                print(f"  {stage.name}: [PROCESSING: {data}]")
            else:
                print(f"  {stage.name}: [WAITING]")
        time.sleep(0.5)

# Program utama
if __name__ == "__main__":
    # Membuat pipeline
    pipeline = Pipeline()
    pipeline.add_stage(PipelineStage("Fetch"))
    pipeline.add_stage(PipelineStage("Decode"))
    pipeline.add_stage(PipelineStage("Execute"))
    pipeline.add_stage(PipelineStage("Write Back"))

    # Input awal
    # input_data = 5
    input_data = random.randint(1, 100)

    # Eksekusi pipeline dengan input
    result = pipeline.execute(input_data)
