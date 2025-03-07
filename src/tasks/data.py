from typing import List
import pandas as pd



import pandas as pd

from ..utils.date import format_date

from ..utils.logger import call_logger



@call_logger('preprocessamento/leitura_dados')
def load_data(pathfile: str) -> pd.DataFrame:
    return pd.read_excel(pathfile)



class Pipeline:

    def __init__(self, df: pd.DataFrame):
        self.df = df
    

    def required(self, required_columns: List[str]) -> bool:
        """
        Valida se as colunas obrigatórias estão presentes e preenchidas.

        Args:
            required_columns (List[str]): Lista de colunas obrigatórias.

        Returns:
            bool: True se todas as colunas estiverem presentes e preenchidas, False caso contrário.
        """
        # Verifica se todas as colunas obrigatórias estão presentes
        missing_columns = [col for col in required_columns if col not in self.df.columns]
        if missing_columns:
            print(f"Erro: As seguintes colunas estão faltando: {missing_columns}")
            return False

        # Verifica se há valores ausentes nas colunas obrigatórias
        missing_values = self.df[required_columns].isnull().any()
        if missing_values.any():
            print(f"Erro: Valores ausentes nas colunas: {missing_values[missing_values].index.tolist()}")
            return False

        print("Todas as colunas obrigatórias estão presentes e preenchidas.")
        return True


    @call_logger('preprocessamento/filtro_aprovados')
    def approved(self) -> pd.DataFrame:
        return self.df.loc[self.df['Status do Pedido'] == 'Aprovado']


    @call_logger('preprocessamento/relatorio_final')
    def formated_report_final(self, approved: pd.DataFrame) -> pd.DataFrame:

        data = []

        for _, row in approved.iterrows():
           
            row['Data do Pedido'] = format_date(row['Data do Pedido'])
            
            data.append(row.to_dict())

        return data

          
