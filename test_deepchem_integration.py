"""
test_deepchem_integration.py
Unit tests for DeepChem integration and property prediction workflow.
"""
import unittest
import os
from deepchem_integration import load_smiles, get_all_properties, ZINC_LOCAL, PROPERTIES  


class TestDeepChemIntegration(unittest.TestCase):
    # Removed test_download_zinc_dataset (no longer needed)
    def test_load_smiles(self):
        smiles_list = load_smiles()
        print("Loaded SMILES count:", len(smiles_list))
        print("First 5 SMILES:", smiles_list[:5])
        self.assertIsInstance(smiles_list, list)
        self.assertGreater(len(smiles_list), 0)
        self.assertIsInstance(smiles_list[0], str)

    def test_get_all_properties_realistic(self):
        # Use first 5 SMILES from the dataset for robust testing
        smiles_list = load_smiles()
        test_smiles = [s for s in smiles_list[:5] if s and isinstance(s, str)]
        for smiles in test_smiles:
            print(f"\nTesting SMILES: {smiles}")
            props = get_all_properties(smiles)
            print("Output:")
            for k, v in props.items():
                print(f"  {k}: {v}")
            # Basic checks
            self.assertIsInstance(props, dict)
            for prop in PROPERTIES:
                self.assertIn(prop, props)

    def test_properties_types(self):
        # Use a realistic SMILES
        smiles = "CCO"  # Ethanol
        props = get_all_properties(smiles)
        # Type checks (some may be None if model not available)
        self.assertTrue(isinstance(props['toxicity'], (float, type(None))))
        self.assertTrue(isinstance(props['solubility'], (float, type(None))))
        self.assertTrue(isinstance(props['bioactivity'], (bool, type(None))))
        self.assertTrue(isinstance(props['permeability'], (float, type(None))))
        self.assertTrue(isinstance(props['logP'], (float, type(None))))
        self.assertTrue(isinstance(props['stability'], (str, type(None))))
        self.assertTrue(isinstance(props['binding_affinity'], (float, type(None))))
        self.assertTrue(isinstance(props['mutagenicity'], (bool, type(None))))
        self.assertTrue(isinstance(props['toxicological_endpoints'], (dict, type(None))))
        self.assertTrue(isinstance(props['custom_hmpi'], (float, type(None))))

if __name__ == "__main__":
    unittest.main()
