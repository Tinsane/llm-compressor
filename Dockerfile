# Start from the Python 3.10 base image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the build directory into the container
COPY . /app

# Install dependencies from the build directory
RUN pip install -r requirements.txt

# Install dependencies from the build directory
RUN pip install .

# Set environment variables required by the script
ENV MODEL_ID=""
ENV SAVE_DIR=""
ENV HF_TOKEN=""

# Command to run the script
CMD ["python", "quant-llmcomp.py"]

