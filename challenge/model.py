from datetime import datetime
from typing import Tuple, Union

import joblib
import numpy as np
import pandas as pd


class DelayModel:
    def __init__(self) -> None:
        self._model = joblib.load("./challenge/delay.model")
        self.features = [
            "OPERA_Latin American Wings",
            "MES_7",
            "MES_10",
            "OPERA_Grupo LATAM",
            "MES_12",
            "TIPOVUELO_I",
            "MES_4",
            "MES_11",
            "OPERA_Sky Airline",
            "OPERA_Copa Air",
        ]
        self.features_raw = ["OPERA", "MES", "TIPOVUELO"]
        self.threshold_in_minutes = 15

    def _get_min_diff(self, data: pd.Series) -> float:
        fecha_o = datetime.strptime(data["Fecha-O"], "%Y-%m-%d %H:%M:%S")
        fecha_i = datetime.strptime(data["Fecha-I"], "%Y-%m-%d %H:%M:%S")
        min_diff = ((fecha_o - fecha_i).total_seconds()) / 60
        return min_diff

    def _get_target(
        self, data: pd.DataFrame, target_column: str
    ) -> pd.DataFrame:
        data["min_diff"] = data.apply(self._get_min_diff, axis=1)
        data[target_column] = np.where(
            data["min_diff"] > self.threshold_in_minutes, 1, 0
        )
        return data[[target_column]]

    def preprocess(
        self, data: pd.DataFrame, target_column: Union[str, None] = None
    ) -> Union[Tuple[pd.DataFrame, pd.DataFrame], pd.DataFrame]:
        """
        Prepare raw data for training or predict.

        Args:
            data (pd.DataFrame): raw data.
            target_column (str, optional): if set, the target is returned.

        Returns:
            Tuple[pd.DataFrame, pd.DataFrame]: features and target.
            or
            pd.DataFrame: features.
        """

        data_to_process = data[self.features_raw]

        rows = []
        for _, row in data_to_process.iterrows():
            new_row = {feature: False for feature in self.features}
            for feature_name in self.features_raw:
                feature_value = row[feature_name]
                if f"{feature_name}_{feature_value}" in new_row:
                    new_row[f"{feature_name}_{feature_value}"] = True
            rows.append(new_row)

        features = pd.DataFrame(rows)

        if not target_column:
            return features

        return features, self._get_target(
            data=data, target_column=target_column
        )

    def fit(self, features: pd.DataFrame, target: pd.DataFrame) -> None:
        """
        Fit model with preprocessed data.

        Args:
            features (pd.DataFrame): preprocessed data.
            target (pd.DataFrame): target.
        """
        return

    def predict(self, features: pd.DataFrame) -> list[int]:
        """
        Predict delays for new flights.

        Args:
            features (pd.DataFrame): preprocessed data.

        Returns:
            (List[int]): predicted targets.
        """
        return self._model.predict(features).astype(int).tolist()
