

import json
import os
from typing import Any, Dict


class MCPDiscovery:
    """
    Reads a JSON config defining the MCP servers and provides access to the server definitions under the mcpServers key
    
    Attributes:
        config_file (str): Path to the JSON configuration file.
        config (Dict[str, Any]): Parsed JSON configuration.
    """
    
    def __init__(self, config_file: str = None):
        """"
        Initializes the MCPDiscovery with a configuration file.
        
        Args:
            config_file (str): Path to the JSON configuration file. If None, defaults to 'utilities/mcp_config.json'.
        """
        if config_file is None:
            self.config_file = os.path.join(os.path.dirname(__file__), 'mcp_config.json')
        
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        try:
            with open(self.config_file, 'r') as file:
                data = json.load(file)
        
            if not isinstance(data, dict):
                raise ValueError("Invalid MCP configuration file format.")

            return data
        except FileNotFoundError:
            raise FileNotFoundError(f"Configuration file '{self.config_file}' not found.")
        except json.JSONDecodeError:
            raise ValueError(f"Error decoding JSON from the configuration file '{self.config_file}'.")
        
    def list_servers(self) -> Dict[str, Any]:
        """
        Lists all MCP servers defined in the configuration.
        
        Returns:
            Dict[str, Any]: A dictionary containing the MCP server definitions.
        """
        if "mcpServers" not in self.config:
            raise KeyError("No 'mcpServers' key found in the configuration file.")
        
        return self.config.get("mcpServers", {})