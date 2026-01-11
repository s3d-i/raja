from __future__ import annotations

import pickle
from pathlib import Path
from typing import Iterable, List, Sequence, Tuple, Union

import pandas as pd

PathLike = Union[str, Path]
Bundle = Sequence[Union[pd.DataFrame, Sequence[pd.DataFrame]]]


def load_df_list_pickle(path: PathLike) -> Bundle:
    """
    Load a pickle that stores a list-based bundle of conversation DataFrames.
    The legacy assets mix list-of-DataFrames and list-of-list-of-DataFrames; this
    function leaves the structure intact for downstream handling.
    """
    path = Path(path)
    with path.open("rb") as fp:
        data = pickle.load(fp)
    return data


def _iter_frames(bundles: Bundle) -> Iterable[Tuple[int, pd.DataFrame]]:
    """
    Yield (conversation_idx, DataFrame) pairs from a bundle.
    Accepts either a list of DataFrames or a list where each element is a list of DataFrames.
    """
    for convo_idx, item in enumerate(bundles):
        if isinstance(item, pd.DataFrame):
            yield convo_idx, item
        elif isinstance(item, (list, tuple)):
            for frame in item:
                if isinstance(frame, pd.DataFrame):
                    yield convo_idx, frame
        else:
            continue


def flatten_conversation_bundles(
    bundles: Bundle, add_conversation_id: bool = True
) -> pd.DataFrame:
    """
    Flatten a conversation bundle into a single DataFrame.

    Parameters
    ----------
    bundles : Bundle
        List of DataFrames or list-of-list-of-DataFrames.
    add_conversation_id : bool
        When True, add a `conversation_idx` column to retain grouping info.
    """
    frames: List[pd.DataFrame] = []
    for convo_idx, frame in _iter_frames(bundles):
        df = frame.copy()
        if add_conversation_id:
            df.insert(0, "conversation_idx", convo_idx)
        frames.append(df)
    if not frames:
        return pd.DataFrame()
    return pd.concat(frames, axis=0)


def describe_bundle(bundles: Bundle, sample_rows: int = 3) -> dict:
    """
    Provide lightweight stats for a conversation bundle to avoid loading everything in notebook output.
    """
    bundle_len = len(bundles)
    frames = list(_iter_frames(bundles))
    column_set = set()
    example_ids: List[str] = []
    for convo_idx, frame in frames:
        column_set.update(frame.columns)
        if len(example_ids) < sample_rows:
            example_ids.extend(frame.index.astype(str).tolist()[:sample_rows - len(example_ids)])
    return {
        "bundle_len": bundle_len,
        "frame_count": len(frames),
        "columns": sorted(column_set),
        "example_ids": example_ids,
    }
