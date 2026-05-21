import re

class RetrospectivePurifier:
    """
    Motor de Purificación Retrospectiva para PMAP.APP.
    Limpia el ruido léxico para asegurar hashes CST deterministas.
    """
    
    @staticmethod
    def purify_code(code: str) -> str:
        """
        Elimina comentarios, docstrings y normaliza espacios 
        sin alterar la estructura funcional del código.
        """
        if not code:
            return ""

        # 1. Eliminar comentarios de una sola línea (#)
        code = re.sub(r'#.*', '', code)

        # 2. Eliminar docstrings y comentarios multilínea (''' o """)
        code = re.sub(r'(\'\'\'|\"\"\")(.*?)(\'\'\'|\"\"\")', '', code, flags=re.DOTALL)

        # 3. Normalizar espacios en blanco (conservando sangrías críticas)
        lines = []
        for line in code.splitlines():
            stripped = line.rstrip()
            if stripped:
                lines.append(stripped)
        
        return "\n".join(lines)

    @staticmethod
    def isolate_canonical_intent(text: str) -> str:
        """
        Aísla la intención semántica del usuario eliminando 
        metadatos de sistema innecesarios.
        """
        # Elimina indicadores de sistema o bloques de herramientas
        text = re.sub(r'\[.*?\]', '', text)
        return text.strip()