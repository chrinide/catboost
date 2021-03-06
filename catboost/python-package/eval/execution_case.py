import json

from catboost import CatboostError
from eval.factor_utils import FactorUtils


class ExecutionCase:

    def __init__(self,
                 params,
                 label=None,
                 ignored_features=None,
                 learning_rate=None):
        """
            Instances of this class are cases cases which will be compared during evaluation
            Params are CatBoost params
            label is string which will be used for plots and other visualisations
            ignored_features is set of additional features to ignore
        """
        case_params = dict(params)

        if learning_rate is not None:
            case_params["learning_rate"] = learning_rate

        all_ignored_features = set()
        if "ignored_features" in case_params:
            all_ignored_features.update(set(case_params["ignored_features"]))
        if ignored_features is not None:
            all_ignored_features.update(ignored_features)

        case_params["ignored_features"] = list(all_ignored_features)

        self._label = label if label is not None else ""
        self._ignored_features = ignored_features
        self._ignored_features_str = FactorUtils.factors_to_ranges_string(self._ignored_features)

        self.__set_params(case_params)

    def __set_params(self, params):
        self._params = params
        self._params_hash = hash(json.dumps(self._params, sort_keys=True))

    def _set_thread_count(self, thread_count):
        params = self._params
        params["thread_count"] = thread_count
        self.__set_params(params)

    @staticmethod
    def _validate_ignored_features(ignored_features, eval_features):
        for eval_feature in eval_features:
            if eval_feature in ignored_features:
                raise CatboostError(
                    "Feature {} is in ignored set and in tmp-features set at the same time".format(eval_feature))

    def get_params(self):
        return dict(self._params)

    def get_label(self):
        return self._label

    def __str__(self):
        if len(self._label) == 0:
            return "Ignore: {}".format(self._ignored_features_str)
        else:
            return '{}, Ignore: {}'.format(self._label, self._ignored_features_str)

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self._params == other._params and self._label == other._label

    def __hash__(self):
        return hash((self._label, self._params_hash))
