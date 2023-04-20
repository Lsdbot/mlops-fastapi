"""
Программа: Сборный конвейер для тренировки модели
Версия: 1.0
"""

from .get_data import get_data
from .train import find_optimal_params, train_model
from .preprocessing import get_supplier_data


def pipeline_training(config, supplier_id):

    preproc = config["preprocessing"]
    train = config["train"]["recommender"]

    train_data = get_data(preproc['train_data'], train['vector'])

    for i in range(preproc['n_components']):
        train_data[str(i)] = train_data[train['vector']].apply(lambda x: x[i])

    train_data = get_supplier_data(train_data, supplier_id, **preproc['recommender'])

    train_data['target'] = train_data.index.isin(
        train_data[train_data[train['sup_column']] == supplier_id][train['index_column']].unique()).astype(int)

    x_train = train_data[train_data.columns[:-1]]
    y_train = train_data['target']

    study = find_optimal_params(x_train, y_train, n_trials=train['n_trials'],
                                N_FOLDS=train['N_FOLDS'], random_state=train['random_state'])

    model = train_model(x_train, y_train, study)

    return model