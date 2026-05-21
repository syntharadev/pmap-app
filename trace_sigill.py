import sys
import os

# Forzamos a Python a mirar dentro de la carpeta core,
# exactamente como lo hace cuando arrancas server.py
sys.path.insert(0, os.path.abspath("pmap_core/pmap"))

print("=== RASTREO DE INSTRUCCIONES ILEGALES (SIGILL) ===")

print("[1] Importando config...")
import config

print("[2] Importando motor de tensores...")
import tensors

print("[3] Importando parser...")
import parser

print("[4] Importando agente PR-CoT...")
import pr_cot_interrogator

print("[5] Importando writer...")
import writer

print("[6] Importando motor semántico (Scikit-learn/NetworkX)...")
import semantic_engine

print("[7] Importando motor CST (Tree-sitter)...")
import cst_diff

print("[8] Importando orquestador core...")
import analyzer

print("[9] Importando servidor FastAPI...")
import server

print("\n[OK] RASTREO LIMPIO. Todo cargó sin colapsar el procesador.")