
from __future__ import annotations
from dataclasses import dataclass


@dataclass(frozen=True)
class PlugReference:
    node_id: str
    attribute_name: str
    
class ConnectionRecord:
    source: PlugReference
    destination: PlugReference
    
