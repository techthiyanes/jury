import pytest

from jury import Jury
from jury.metrics import AutoMetric
from tests.jury.conftest import get_expected_output
from tests.utils import assert_almost_equal_dict


@pytest.fixture(scope="module")
def jury_bartscore():
    metric = AutoMetric.load("bartscore", device="cpu")
    return Jury(metrics=metric)


@pytest.fixture(scope="module")
def jury_bartscore_segment():
    metric = AutoMetric.load("bartscore", device="cpu", compute_kwargs={"segment_scores": True})
    return Jury(metrics=metric)


@pytest.fixture
@get_expected_output(prefix="metrics")
def output_basic():
    return output_basic.output


@pytest.fixture
@get_expected_output(prefix="metrics")
def output_basic_segment():
    return output_basic_segment.output


@pytest.fixture
@get_expected_output(prefix="metrics")
def output_multiple_ref():
    return output_multiple_ref.output


@pytest.fixture
@get_expected_output(prefix="metrics")
def output_multiple_pred_multiple_ref():
    return output_multiple_pred_multiple_ref.output


def test_basic(predictions, references, jury_bartscore, output_basic):
    scores = jury_bartscore(predictions=predictions, references=references)
    assert_almost_equal_dict(actual=scores, desired=output_basic)


def test_basic_segment(predictions, references, jury_bartscore_segment, output_basic_segment):
    scores = jury_bartscore_segment(predictions=predictions, references=references)
    assert_almost_equal_dict(actual=scores, desired=output_basic_segment)


def test_multiple_ref(predictions, multiple_references, jury_bartscore, output_multiple_ref):
    scores = jury_bartscore(predictions=predictions, references=multiple_references)
    assert_almost_equal_dict(actual=scores, desired=output_multiple_ref)


def test_multiple_pred_multiple_ref(
    multiple_predictions, multiple_references, jury_bartscore, output_multiple_pred_multiple_ref
):
    scores = jury_bartscore(predictions=multiple_predictions, references=multiple_references)
    assert_almost_equal_dict(actual=scores, desired=output_multiple_pred_multiple_ref)
