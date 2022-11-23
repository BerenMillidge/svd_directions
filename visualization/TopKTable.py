from typing import List, Union
try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal

import numpy as np
import torch

Tensor = Union[np.ndarray, torch.Tensor]

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def init(
    tokens: List[str],
    activations: Tensor,
    obj_type: str,
    layer_labels=None,
    obj_labels=None,
    k=10,
    filter: Literal["topk", "bottomk", "topk+bottomk"] = "topk",
):
    """Visualize the top-k tokens and their corresponding activation strength
    in table format for a set of objects such as SVD directions or neurons.

    Args:
      tokens: a list of strings representing tokens.
      activations: A [n_tokens, n_layers, n_objects_per_layer] array representing activation values.
      obj_type: A string representing the type of object. For example, "Neuron" or "SVD direction".
      layer_labels: (optional) human readable labels for the given layers.
      obj_labels: (optional) human readable labels for the given objects.
      k = 10: The number of tokens to show for each object.
      filter = "topk": The filter to use for selecting the top-k tokens. Can be "topk" or "threshold".
    """
    assert filter in ["topk", "bottomk", "topk+bottomk"]
    assert isinstance(obj_type, str), "obj_type must be a string"
    assert (
        len(tokens) == activations.shape[0]
    ), "tokens and activations must be same length"
    assert (
        len(activations.shape) == 3
    ), "activations must be of the form [n_tokens, n_layers, n_objects_per_layer]"
    if layer_labels is None:
        layer_labels = [str(layer) for layer in range(activations.shape[1])]
    else:
        assert (
            len(layer_labels) == activations.shape[1]
        ), "layer_labels must correspond to number of layers in the activations"

    if obj_labels is None:
        obj_labels = [str(obj) for obj in range(activations.shape[2])]
    else:
        assert (
            len(obj_labels) == activations.shape[2]
        ), "obj_labels must correspond to number of objects in the activations"

    # get topk tokens for each object
    activations_tensor = torch.tensor(activations).to(device)
    topk_vals, topk_inds = activations_tensor.topk(k=k, dim=0)

    # also get bottom k vals
    bottomk_vals, bottomk_inds = activations_tensor.topk(k=k, dim=0, largest=False)

    # reverse sort order of bottomk vals and inds
    bottomk_vals = bottomk_vals.flip(0)
    bottomk_inds = bottomk_inds.flip(0)

    filter = (
        None if filter == "topk+bottomk" else filter
    )  # defaults to topk+bottomk if filter is None
    return {
        "tokens": tokens,
        "obj_type": obj_type,
        "layer_labels": layer_labels,
        "obj_labels": obj_labels,
        "topk_vals": topk_vals,
        "topk_inds": topk_inds,
        "bottomk_vals": bottomk_vals,
        "bottomk_inds": bottomk_inds,
        "filter": filter,
    }
