import os

from packaging import version
import tensorflow
import pytest

from sparseml.tensorflow_v1.datasets import (
    DatasetRegistry,
    ImagenetteDataset,
    ImagewoofDataset,
    ImageFolderDataset,
    create_split_iterators_handle,
)

from sparseml.tensorflow_v1.utils import tf_compat


def _validate(dataset: ImageFolderDataset, size: int):
    with tf_compat.Graph().as_default() as graph:
        batch_size = 16

        with tf_compat.device("/cpu:0"):
            print("loading datasets")
            dataset_len = len(dataset)
            assert dataset_len > 0
            tf_dataset = dataset.build(
                batch_size,
                repeat_count=2,
                shuffle_buffer_size=10,
                prefetch_buffer_size=batch_size,
                num_parallel_calls=4,
            )

        handle, iterator, (tf_iter,) = create_split_iterators_handle([tf_dataset])
        images, labels = iterator.get_next()

        with tf_compat.Session() as sess:
            sess.run(
                [
                    tf_compat.global_variables_initializer(),
                    tf_compat.local_variables_initializer(),
                ]
            )
            iter_handle = sess.run(tf_iter.string_handle())
            sess.run(tf_iter.initializer)

            for _ in range(5):
                batch_x, batch_lab = sess.run(
                    [images, labels], feed_dict={handle: iter_handle}
                )
                assert batch_x.shape[0] == 16
                assert batch_x.shape[1] == size
                assert batch_x.shape[2] == size
                assert batch_x.shape[3] == 3
                assert batch_lab.shape[0] == 16
                assert batch_lab.shape[1] == 10


@pytest.mark.skipif(
    os.getenv("NM_ML_SKIP_TENSORFLOW_TESTS", False), reason="Skipping tensorflow_v1 tests",
)
@pytest.mark.skipif(
    version.parse(tensorflow.__version__) < version.parse("1.3"),
    reason="Must install tensorflow_v1 version 1.3 or greater",
)
@pytest.mark.skipif(
    os.getenv("NM_ML_SKIP_DATASET_TESTS", False), reason="Skipping dataset tests",
)
def test_imagenette_160():
    train_dataset = ImagenetteDataset(train=True)
    _validate(train_dataset, 160)

    val_dataset = ImagenetteDataset(train=False)
    _validate(val_dataset, 160)

    reg_dataset = DatasetRegistry.create("imagenette", train=False)
    _validate(reg_dataset, 160)


@pytest.mark.skipif(
    os.getenv("NM_ML_SKIP_TENSORFLOW_TESTS", False), reason="Skipping tensorflow_v1 tests",
)
@pytest.mark.skipif(
    version.parse(tensorflow.__version__) < version.parse("1.3"),
    reason="Must install tensorflow_v1 version 1.3 or greater",
)
@pytest.mark.skipif(
    os.getenv("NM_ML_SKIP_DATASET_TESTS", False), reason="Skipping dataset tests",
)
def test_imagewoof_160():
    train_dataset = ImagewoofDataset(train=True)
    _validate(train_dataset, 160)

    val_dataset = ImagewoofDataset(train=False)
    _validate(val_dataset, 160)

    reg_dataset = DatasetRegistry.create("imagewoof", train=False)
    _validate(reg_dataset, 160)
