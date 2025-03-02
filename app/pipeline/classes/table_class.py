import os
import sys

sys.path.append(os.path.abspath(os.path.dirname(__file__)))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "pipeline")))

from abc import ABC, abstractmethod
from typing import Dict
import json


class Table(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def build_table(self, params: Dict) -> json:
        raise NotImplementedError("Method 'search_movie' not implemented")
    
    @abstractmethod
    def get_teams(self, params: Dict) -> json:
        raise NotImplementedError("Method 'search_movie' not implemented")
    
    @abstractmethod
    def get_results(self) -> Dict:
        raise NotImplementedError("Method 'search_movie' not implemented")

    @abstractmethod
    def build_table():
        raise NotImplementedError("Method 'build_object' not implemented")
