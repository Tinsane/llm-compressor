import pytest

import os
import json
from typing import List
from collections import OrderedDict, namedtuple
import torch

from neuralmagicML.pytorch.utils import ModuleExporter
from neuralmagicML.utils import RepoModel
from tests.pytorch.helpers import LinearNet, MLPNet, ConvNet

__all__ = ["extract_node_models", "analyzer_models", "onnx_repo_models", "analyzer_models_repo"]


TEMP_FOLDER = os.path.expanduser(os.path.join("~", ".cache", "nm_models"))


@pytest.fixture(
    params=[
        (
            "test_linear_net",
            LinearNet,
            torch.randn(8),
            {
                "output": ([[8]], [[8]]),
                "10": ([[8]], [[16]]),
                "11": ([[16]], [[16]]),
                "13": ([[16]], [[32]]),
                "14": ([[32]], [[32]]),
                "16": ([[32]], [[16]]),
                "17": ([[16]], [[16]]),
                "19": ([[16]], [[8]]),
                "input": (None, [[8]]),
            },
        ),
        (
            "test_mlp_net",
            MLPNet,
            torch.randn(8),
            {
                "output": ([[64]], [[64]]),
                "8": ([[8]], [[16]]),
                "9": ([[16]], [[16]]),
                "10": ([[16]], [[16]]),
                "12": ([[16]], [[32]]),
                "13": ([[32]], [[32]]),
                "14": ([[32]], [[32]]),
                "16": ([[32]], [[64]]),
                "17": ([[64]], [[64]]),
                "input": (None, [[8]]),
            },
        ),
        (
            "test_conv_net",
            ConvNet,
            torch.randn(16, 3, 3, 3),
            {
                "output": ([[16, 10]], [[16, 10]]),
                "7": ([[16, 3, 3, 3]], [[16, 16, 2, 2]]),
                "8": ([[16, 16, 2, 2]], [[16, 16, 2, 2]]),
                "9": ([[16, 16, 2, 2]], [[16, 32, 1, 1]]),
                "10": ([[16, 32, 1, 1]], [[16, 32, 1, 1]]),
                "11": ([[16, 32, 1, 1]], [[16, 32, 1, 1]]),
                "12": ([[16, 32, 1, 1]], [[4]]),
                "13": (None, None),
                "14": ([[4]], None),
                "16": (None, [[1]]),
                "18": ([[1]], [[2]]),
                "19": ([[16, 32, 1, 1], [2]], [[16, 32]]),
                "20": ([[16, 32]], [[16, 10]]),
                "input": (None, [[16, 3, 3, 3]]),
            },
        ),
    ]
)
def extract_node_models(request):
    model_name, model_function, sample_batch, expected_output = request.param
    directory = os.path.join(TEMP_FOLDER, model_name)
    os.makedirs(directory, exist_ok=True)
    model_path = os.path.join(directory, "model.onnx")

    if not os.path.exists(model_path):
        module = model_function()
        exporter = ModuleExporter(module, directory)
        exporter.export_onnx(sample_batch=sample_batch)
    return os.path.expanduser(model_path), expected_output


# TODO update when flops are done
@pytest.fixture(
    params=[
        (
            "test_linear_net",
            LinearNet,
            torch.randn(8),
            {
                "nodes": [
                    {
                        "id": "10",
                        "op_type": "MatMul",
                        "input_names": ["input"],
                        "output_names": ["10"],
                        "input_shapes": [[8]],
                        "output_shapes": [[16]],
                        "params": 128,
                        "prunable": True,
                        "prunable_params": 128,
                        "prunable_params_zeroed": 0,
                        "flops": 256,
                        "weight_name": "21",
                        "weight_shape": [8, 16],
                        "bias_name": None,
                        "bias_shape": None,
                        "attributes": {},
                    },
                    {
                        "id": "11",
                        "op_type": "Add",
                        "input_names": ["10"],
                        "output_names": ["11"],
                        "input_shapes": [[16]],
                        "output_shapes": [[16]],
                        "params": 0,
                        "prunable": False,
                        "prunable_params": -1,
                        "prunable_params_zeroed": 0,
                        "flops": 16,
                        "weight_name": None,
                        "weight_shape": None,
                        "bias_name": None,
                        "bias_shape": None,
                        "attributes": {},
                    },
                    {
                        "id": "13",
                        "op_type": "MatMul",
                        "input_names": ["11"],
                        "output_names": ["13"],
                        "input_shapes": [[16]],
                        "output_shapes": [[32]],
                        "params": 512,
                        "prunable": True,
                        "prunable_params": 512,
                        "prunable_params_zeroed": 0,
                        "flops": 1024,
                        "weight_name": "22",
                        "weight_shape": [16, 32],
                        "bias_name": None,
                        "bias_shape": None,
                        "attributes": {},
                    },
                    {
                        "id": "14",
                        "op_type": "Add",
                        "input_names": ["13"],
                        "output_names": ["14"],
                        "input_shapes": [[32]],
                        "output_shapes": [[32]],
                        "params": 0,
                        "prunable": False,
                        "prunable_params": -1,
                        "prunable_params_zeroed": 0,
                        "flops": 32,
                        "weight_name": None,
                        "weight_shape": None,
                        "bias_name": None,
                        "bias_shape": None,
                        "attributes": {},
                    },
                    {
                        "id": "16",
                        "op_type": "MatMul",
                        "input_names": ["14"],
                        "output_names": ["16"],
                        "input_shapes": [[32]],
                        "output_shapes": [[16]],
                        "params": 512,
                        "prunable": True,
                        "prunable_params": 512,
                        "prunable_params_zeroed": 0,
                        "flops": 1024,
                        "weight_name": "23",
                        "weight_shape": [32, 16],
                        "bias_name": None,
                        "bias_shape": None,
                        "attributes": {},
                    },
                    {
                        "id": "17",
                        "op_type": "Add",
                        "input_names": ["16"],
                        "output_names": ["17"],
                        "input_shapes": [[16]],
                        "output_shapes": [[16]],
                        "params": 0,
                        "prunable": False,
                        "prunable_params": -1,
                        "prunable_params_zeroed": 0,
                        "flops": 16,
                        "weight_name": None,
                        "weight_shape": None,
                        "bias_name": None,
                        "bias_shape": None,
                        "attributes": {},
                    },
                    {
                        "id": "19",
                        "op_type": "MatMul",
                        "input_names": ["17"],
                        "output_names": ["19"],
                        "input_shapes": [[16]],
                        "output_shapes": [[8]],
                        "params": 128,
                        "prunable": True,
                        "prunable_params": 128,
                        "prunable_params_zeroed": 0,
                        "flops": 256,
                        "weight_name": "24",
                        "weight_shape": [16, 8],
                        "bias_name": None,
                        "bias_shape": None,
                        "attributes": {},
                    },
                    {
                        "id": "output",
                        "op_type": "Add",
                        "input_names": ["19"],
                        "output_names": ["output"],
                        "input_shapes": [[8]],
                        "output_shapes": [[8]],
                        "params": 0,
                        "prunable": False,
                        "prunable_params": -1,
                        "prunable_params_zeroed": 0,
                        "flops": 8,
                        "weight_name": None,
                        "weight_shape": None,
                        "bias_name": None,
                        "bias_shape": None,
                        "attributes": {},
                    },
                ]
            },
        ),
        (
            "test_mlp_net",
            MLPNet,
            torch.randn(8),
            {
                "nodes": [
                    {
                        "id": "8",
                        "op_type": "MatMul",
                        "input_names": ["input"],
                        "output_names": ["8"],
                        "input_shapes": [[8]],
                        "output_shapes": [[16]],
                        "params": 128,
                        "prunable": True,
                        "prunable_params": 128,
                        "prunable_params_zeroed": 0,
                        "flops": 256,
                        "weight_name": "19",
                        "weight_shape": [8, 16],
                        "bias_name": None,
                        "bias_shape": None,
                        "attributes": {},
                    },
                    {
                        "id": "9",
                        "op_type": "Add",
                        "input_names": ["8"],
                        "output_names": ["9"],
                        "input_shapes": [[16]],
                        "output_shapes": [[16]],
                        "params": 0,
                        "prunable": False,
                        "prunable_params": -1,
                        "prunable_params_zeroed": 0,
                        "flops": 16,
                        "weight_name": None,
                        "weight_shape": None,
                        "bias_name": None,
                        "bias_shape": None,
                        "attributes": {},
                    },
                    {
                        "id": "10",
                        "op_type": "Relu",
                        "input_names": ["9"],
                        "output_names": ["10"],
                        "input_shapes": [[16]],
                        "output_shapes": [[16]],
                        "params": 0,
                        "prunable": False,
                        "prunable_params": -1,
                        "prunable_params_zeroed": 0,
                        "flops": 16,
                        "weight_name": None,
                        "weight_shape": None,
                        "bias_name": None,
                        "bias_shape": None,
                        "attributes": {},
                    },
                    {
                        "id": "12",
                        "op_type": "MatMul",
                        "input_names": ["10"],
                        "output_names": ["12"],
                        "input_shapes": [[16]],
                        "output_shapes": [[32]],
                        "params": 512,
                        "prunable": True,
                        "prunable_params": 512,
                        "prunable_params_zeroed": 0,
                        "flops": 1024,
                        "weight_name": "20",
                        "weight_shape": [16, 32],
                        "bias_name": None,
                        "bias_shape": None,
                        "attributes": {},
                    },
                    {
                        "id": "13",
                        "op_type": "Add",
                        "input_names": ["12"],
                        "output_names": ["13"],
                        "input_shapes": [[32]],
                        "output_shapes": [[32]],
                        "params": 0,
                        "prunable": False,
                        "prunable_params": -1,
                        "prunable_params_zeroed": 0,
                        "flops": 32,
                        "weight_name": None,
                        "weight_shape": None,
                        "bias_name": None,
                        "bias_shape": None,
                        "attributes": {},
                    },
                    {
                        "id": "14",
                        "op_type": "Relu",
                        "input_names": ["13"],
                        "output_names": ["14"],
                        "input_shapes": [[32]],
                        "output_shapes": [[32]],
                        "params": 0,
                        "prunable": False,
                        "prunable_params": -1,
                        "prunable_params_zeroed": 0,
                        "flops": 32,
                        "weight_name": None,
                        "weight_shape": None,
                        "bias_name": None,
                        "bias_shape": None,
                        "attributes": {},
                    },
                    {
                        "id": "16",
                        "op_type": "MatMul",
                        "input_names": ["14"],
                        "output_names": ["16"],
                        "input_shapes": [[32]],
                        "output_shapes": [[64]],
                        "params": 2048,
                        "prunable": True,
                        "prunable_params": 2048,
                        "prunable_params_zeroed": 0,
                        "flops": 4096,
                        "weight_name": "21",
                        "weight_shape": [32, 64],
                        "bias_name": None,
                        "bias_shape": None,
                        "attributes": {},
                    },
                    {
                        "id": "17",
                        "op_type": "Add",
                        "input_names": ["16"],
                        "output_names": ["17"],
                        "input_shapes": [[64]],
                        "output_shapes": [[64]],
                        "params": 0,
                        "prunable": False,
                        "prunable_params": -1,
                        "prunable_params_zeroed": 0,
                        "flops": 64,
                        "weight_name": None,
                        "weight_shape": None,
                        "bias_name": None,
                        "bias_shape": None,
                        "attributes": {},
                    },
                    {
                        "id": "output",
                        "op_type": "Sigmoid",
                        "input_names": ["17"],
                        "output_names": ["output"],
                        "input_shapes": [[64]],
                        "output_shapes": [[64]],
                        "params": 0,
                        "prunable": False,
                        "prunable_params": -1,
                        "prunable_params_zeroed": 0,
                        "flops": 64,
                        "weight_name": None,
                        "weight_shape": None,
                        "bias_name": None,
                        "bias_shape": None,
                        "attributes": {},
                    },
                ]
            },
        ),
        (
            "test_conv_net",
            ConvNet,
            torch.randn(16, 3, 3, 3),
            {
                "nodes": [
                    {
                        "id": "7",
                        "op_type": "Conv",
                        "input_names": ["input"],
                        "output_names": ["7"],
                        "input_shapes": [[16, 3, 3, 3]],
                        "output_shapes": [[16, 16, 2, 2]],
                        "params": 448,
                        "prunable": True,
                        "prunable_params": 432,
                        "prunable_params_zeroed": 0,
                        "flops": 27712,
                        "weight_name": "seq.conv1.weight",
                        "weight_shape": [16, 3, 3, 3],
                        "bias_name": "seq.conv1.bias",
                        "bias_shape": [16],
                        "attributes": {
                            "dilations": [1, 1],
                            "group": 1,
                            "kernel_shape": [3, 3],
                            "pads": [1, 1, 1, 1],
                            "strides": [2, 2],
                        },
                    },
                    {
                        "id": "8",
                        "op_type": "Relu",
                        "input_names": ["7"],
                        "output_names": ["8"],
                        "input_shapes": [[16, 16, 2, 2]],
                        "output_shapes": [[16, 16, 2, 2]],
                        "params": 0,
                        "prunable": False,
                        "prunable_params": -1,
                        "prunable_params_zeroed": 0,
                        "flops": 1024,
                        "weight_name": None,
                        "weight_shape": None,
                        "bias_name": None,
                        "bias_shape": None,
                        "attributes": {},
                    },
                    {
                        "id": "9",
                        "op_type": "Conv",
                        "input_names": ["8"],
                        "output_names": ["9"],
                        "input_shapes": [[16, 16, 2, 2]],
                        "output_shapes": [[16, 32, 1, 1]],
                        "params": 4640,
                        "prunable": True,
                        "prunable_params": 4608,
                        "prunable_params_zeroed": 0,
                        "flops": 73760,
                        "weight_name": "seq.conv2.weight",
                        "weight_shape": [32, 16, 3, 3],
                        "bias_name": "seq.conv2.bias",
                        "bias_shape": [32],
                        "attributes": {
                            "dilations": [1, 1],
                            "group": 1,
                            "kernel_shape": [3, 3],
                            "pads": [1, 1, 1, 1],
                            "strides": [2, 2],
                        },
                    },
                    {
                        "id": "10",
                        "op_type": "Relu",
                        "input_names": ["9"],
                        "output_names": ["10"],
                        "input_shapes": [[16, 32, 1, 1]],
                        "output_shapes": [[16, 32, 1, 1]],
                        "params": 0,
                        "prunable": False,
                        "prunable_params": -1,
                        "prunable_params_zeroed": 0,
                        "flops": 512,
                        "weight_name": None,
                        "weight_shape": None,
                        "bias_name": None,
                        "bias_shape": None,
                        "attributes": {},
                    },
                    {
                        "id": "11",
                        "op_type": "GlobalAveragePool",
                        "input_names": ["10"],
                        "output_names": ["11"],
                        "input_shapes": [[16, 32, 1, 1]],
                        "output_shapes": [[16, 32, 1, 1]],
                        "params": 0,
                        "prunable": False,
                        "prunable_params": -1,
                        "prunable_params_zeroed": 0,
                        "flops": 512,
                        "weight_name": None,
                        "weight_shape": None,
                        "bias_name": None,
                        "bias_shape": None,
                        "attributes": {},
                    },
                    {
                        "id": "12",
                        "op_type": "Shape",
                        "input_names": ["11"],
                        "output_names": ["12"],
                        "input_shapes": [[16, 32, 1, 1]],
                        "output_shapes": [[4]],
                        "params": 0,
                        "prunable": False,
                        "prunable_params": -1,
                        "prunable_params_zeroed": 0,
                        "flops": None,
                        "weight_name": None,
                        "weight_shape": None,
                        "bias_name": None,
                        "bias_shape": None,
                        "attributes": {},
                    },
                    {
                        "id": "13",
                        "op_type": "Constant",
                        "input_names": [],
                        "output_names": ["13"],
                        "input_shapes": None,
                        "output_shapes": None,
                        "params": 0,
                        "prunable": False,
                        "prunable_params": -1,
                        "prunable_params_zeroed": 0,
                        "flops": None,
                        "weight_name": None,
                        "weight_shape": None,
                        "bias_name": None,
                        "bias_shape": None,
                        "attributes": {"value": None},
                    },
                    {
                        "id": "14",
                        "op_type": "Gather",
                        "input_names": ["12", "13"],
                        "output_names": ["14"],
                        "input_shapes": [[4]],
                        "output_shapes": None,
                        "params": 0,
                        "prunable": False,
                        "prunable_params": -1,
                        "prunable_params_zeroed": 0,
                        "flops": None,
                        "weight_name": None,
                        "weight_shape": None,
                        "bias_name": None,
                        "bias_shape": None,
                        "attributes": {"axis": 0},
                    },
                    {
                        "id": "16",
                        "op_type": "Unsqueeze",
                        "input_names": ["14"],
                        "output_names": ["16"],
                        "input_shapes": None,
                        "output_shapes": [[1]],
                        "params": 0,
                        "prunable": False,
                        "prunable_params": -1,
                        "prunable_params_zeroed": 0,
                        "flops": None,
                        "weight_name": None,
                        "weight_shape": None,
                        "bias_name": None,
                        "bias_shape": None,
                        "attributes": {"axes": [0]},
                    },
                    {
                        "id": "18",
                        "op_type": "Concat",
                        "input_names": ["16"],
                        "output_names": ["18"],
                        "input_shapes": [[1]],
                        "output_shapes": [[2]],
                        "params": 0,
                        "prunable": False,
                        "prunable_params": -1,
                        "prunable_params_zeroed": 0,
                        "flops": None,
                        "weight_name": None,
                        "weight_shape": None,
                        "bias_name": None,
                        "bias_shape": None,
                        "attributes": {"axis": 0},
                    },
                    {
                        "id": "19",
                        "op_type": "Reshape",
                        "input_names": ["11", "18"],
                        "output_names": ["19"],
                        "input_shapes": [[16, 32, 1, 1], [2]],
                        "output_shapes": [[16, 32]],
                        "params": 0,
                        "prunable": False,
                        "prunable_params": -1,
                        "prunable_params_zeroed": 0,
                        "flops": None,
                        "weight_name": None,
                        "weight_shape": None,
                        "bias_name": None,
                        "bias_shape": None,
                        "attributes": {},
                    },
                    {
                        "id": "20",
                        "op_type": "Gemm",
                        "input_names": ["19"],
                        "output_names": ["20"],
                        "input_shapes": [[16, 32]],
                        "output_shapes": [[16, 10]],
                        "params": 330,
                        "prunable": True,
                        "prunable_params": 320,
                        "prunable_params_zeroed": 0,
                        "flops": 650,
                        "weight_name": "mlp.fc.weight",
                        "weight_shape": [10, 32],
                        "bias_name": "mlp.fc.bias",
                        "bias_shape": [10],
                        "attributes": {"alpha": 1.0, "beta": 1.0, "transB": 1},
                    },
                    {
                        "id": "output",
                        "op_type": "Sigmoid",
                        "input_names": ["20"],
                        "output_names": ["output"],
                        "input_shapes": [[16, 10]],
                        "output_shapes": [[16, 10]],
                        "params": 0,
                        "prunable": False,
                        "prunable_params": -1,
                        "prunable_params_zeroed": 0,
                        "flops": 160,
                        "weight_name": None,
                        "weight_shape": None,
                        "bias_name": None,
                        "bias_shape": None,
                        "attributes": {},
                    },
                ]
            },
        ),
    ]
)
def analyzer_models(request):
    model_name, model_function, sample_batch, expected_output = request.param
    directory = os.path.join(TEMP_FOLDER, model_name)
    os.makedirs(directory, exist_ok=True)
    model_path = os.path.join(directory, "model.onnx")

    if not os.path.exists(model_path):
        module = model_function()
        exporter = ModuleExporter(module, directory)
        exporter.export_onnx(sample_batch=sample_batch)
    return os.path.expanduser(model_path), expected_output


@pytest.fixture(
    params=[
        (
            {
                "domain": "cv",
                "sub_domain": "classification",
                "architecture": "resnet-v1",
                "sub_architecture": "50",
                "dataset": "imagenet",
                "framework": "pytorch",
                "desc": "base",
            }
        ),
        (
            {
                "domain": "cv",
                "sub_domain": "classification",
                "architecture": "mobilenet-v1",
                "sub_architecture": "1.0",
                "dataset": "imagenet",
                "framework": "pytorch",
                "desc": "base",
            }
        ),
    ]
)
def onnx_repo_models(request):
    model_args = request.param
    model = RepoModel(**model_args)
    model_path = model.download_onnx_file(overwrite=False)
    return model_path

@pytest.fixture(
    params=[
        (
            {
                "domain": "cv",
                "sub_domain": "classification",
                "architecture": "resnet-v1",
                "sub_architecture": "50",
                "dataset": "imagenet",
                "framework": "pytorch",
                "desc": "base",
            },
            "tests/onnx/recal/test_analyzer_model_data/resnet50pytorch.json",
        ),
        (
            {
                "domain": "cv",
                "sub_domain": "classification",
                "architecture": "resnet-v1",
                "sub_architecture": "50",
                "dataset": "imagenet",
                "framework": "tensorflow",
                "desc": "base",
            },
            "tests/onnx/recal/test_analyzer_model_data/resnet50tensorflow.json",
        ),
    ]
)
def analyzer_models_repo(request):
    model_args, output_path = request.param
    model = RepoModel(**model_args)
    model_path = model.download_onnx_file(overwrite=False)

    output = {}
    with open(output_path) as output_file:
        output = dict(json.load(output_file))
    return model_path, output
