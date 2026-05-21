# Copyright (c) 2026 syntharadev (syntharadev@gmail.com)
# Todos los derechos reservados. Licencia: GNU AGPLv3
import re
from typing import List, Dict, Any

class ForensicJSONParser:
    def purify_json_data(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        ruta_canonica = []
        for i, turn in enumerate(data):
            role = turn.get("role", "unknown")
            if "parts" in turn:
                content = "".join([p.get("text", "") for p in turn["parts"]])
            else:
                content = turn.get("content", "")
                
            ruta_canonica.append({
                "turn_index": i,
                "role": role,
                "content": content
            })
        return ruta_canonica

class HeuristicTextParser:
    def parse_raw_clipboard(self, raw_text: str) -> List[Dict[str, Any]]:
        if not raw_text or not raw_text.strip():
            return []
        
        pattern = r'(?m)^\s*(?:\*\*|)?(Tú|Usuario|Gemini|Assistant|Modelo|Asistente)(?:\*\*|)?\s*:?\s*$'
        segments = re.split(pattern, raw_text, flags=re.IGNORECASE)
        ruta_canonica = []
        
        if segments[0].strip():
            ruta_canonica.append({"role": "user", "content": segments[0].strip()})

        for i in range(1, len(segments) - 1, 2):
            role_marker = segments[i].lower()
            content = segments[i+1].strip()
            if not content: continue
            
            role = "user" if any(x in role_marker for x in ["tú", "usuario", "user"]) else "model"
            ruta_canonica.append({"role": role, "content": content})

        optimized_route = []
        for node in ruta_canonica:
            if optimized_route and optimized_route[-1]["role"] == node["role"]:
                optimized_route[-1]["content"] += "\n\n" + node["content"]
            else:
                optimized_route.append(node)
        return optimized_route
