from abc import ABC, abstractmethod
from pathlib import Path
import pandas as pd
from sqlalchemy.orm import Session

class BaseLoader(ABC):
    def __init__(self,session: Session,data_dir:Path):
        self.session = session
        self.data_dir = data_dir
    @property
    @abstractmethod
    def filename(self) -> str:
        pass

    @abstractmethod
    def load(self) -> None:
        pass

    def read_csv(self) -> pd.DataFrame:
        path = self.data_dir / self.filename
        if not path.exists():
            raise FileNotFoundError(f"{path} not found.")
        return pd.read_csv(path)
            

