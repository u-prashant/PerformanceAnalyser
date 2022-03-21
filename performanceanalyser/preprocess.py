from constants import Column

import numpy as np


class Preprocess:
    @staticmethod
    def preprocess(df):
        numeric_df = df.select_dtypes(np.number)
        df[numeric_df.columns] = numeric_df.fillna(0).astype('int')

        df[Column.DS_A2] = df[Column.DS_A2] + df[Column.DS_Rework_A2]
        df[Column.DS_A14] = df[Column.DS_A14] + df[Column.DS_Rework_A14]
        df[Column.DS_A15] = df[Column.DS_A14] + df[Column.DS_Rework_A15]

        df[Column.TS_A14] = df[Column.TS_A14] + df[Column.TS_Rework_A14]
        df[Column.TS_A15] = df[Column.TS_A14] + df[Column.TS_Rework_A15]

        df[Column.Inventory] = df.apply(lambda x:
                                        x[Column.LW] if x[Column.LW] > x[Column.Inventory] else x[Column.Inventory],
                                        axis=1)
        return df
