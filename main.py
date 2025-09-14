import json
import re
from typing import List, Dict, Any

class HeavyMetalReactionEngine:
    def __init__(self, registry_path: str):
        with open(registry_path, 'r') as f:
            self.registry = json.load(f)

    def simulate_reactions(self, input_metals: List[str], environment: Dict[str, Any]) -> List[Dict[str, Any]]:
        compounds = input_metals.copy()
        reaction_chain = []
        max_depth = 10  # To avoid infinite loops

        for _ in range(max_depth):
            reaction_applied = False

            for element_block in self.registry:
                # Heavy metal reactions
                for reaction_eq in element_block.get("reactions_with_heavy_metals", []):
                    try:
                        reactants = self._extract_reactants(reaction_eq)
                        product = self._extract_product(reaction_eq)
                    except ValueError:
                        print(f"[Warning] Skipping malformed equation: {reaction_eq}")
                        continue

                    if all(r in compounds for r in reactants) and product not in compounds:
                        compounds.append(product)
                        reaction_chain.append({
                            "equation": reaction_eq,
                            "type": "heavy_metal",
                            "product": product
                        })
                        reaction_applied = True
                        break  # Apply only one reaction per iteration

                if reaction_applied:
                    break  # Restart loop after applying one reaction

                # Environment reactions
                for reaction_eq in element_block.get("reactions_with_environment", []):
                    try:
                        reactants = self._extract_reactants(reaction_eq)
                        product = self._extract_product(reaction_eq)
                    except ValueError:
                        print(f"[Warning] Skipping malformed equation: {reaction_eq}")
                        continue  # Skip this reaction

                    if all(r in compounds for r in reactants) and product not in compounds:
                        compounds.append(product)
                        reaction_chain.append({
                            "equation": reaction_eq,
                            "type": "environment",
                            "product": product
                        })
                        reaction_applied = True
                        break

                if reaction_applied:
                    break

            if not reaction_applied:
                break  

        return reaction_chain

    def _normalize_arrows(self, equation: str) -> str:
        print(f"Normalizing equation: {equation.encode('unicode_escape')}")
        equation = equation.replace('→', '->').replace('\u2192', '->').replace('\u2794', '->').replace('\u2013', '->')
        return equation

    def _extract_reactants(self, equation: str) -> List[str]:
        equation = self._normalize_arrows(equation.strip())
        parts = equation.split('->')
        if len(parts) < 2:
            raise ValueError(f"Malformed equation (no arrow found): '{equation}'")
        left_side = parts[0]
        return [x.strip() for x in left_side.split('+') if x.strip()]

    def _extract_product(self, equation: str) -> str:
        equation = self._normalize_arrows(equation.strip())
        parts = equation.split('->')
        if len(parts) < 2:
            raise ValueError(f"Malformed equation (no product found): '{equation}'")
        return parts[1].strip()

# Example usage !!!!
if __name__ == "__main__":
    engine = HeavyMetalReactionEngine('reactions.json')

    input_metals = ["As", "O2", "Cd", "SO4", "H2O"]  
    environment = {
        "temperature": 30,
        "humidity": 60
    }

    result = engine.simulate_reactions(input_metals, environment)

    print("\nReaction Chain Results:")
    for idx, step in enumerate(result):
        print(f"{idx+1}. {step['equation']} -> Product: {step['product']} ({step['type']})")