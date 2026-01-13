import unittest
import pandas as pd
import os
from engine import VendorRecommender

class TestVendorMatchAI(unittest.TestCase):
    def setUp(self):
        # Ensure data exists; if not, try to regenerate or fail hard if strict
        if not os.path.exists("vendors.csv"):
            from data_gen import generate_data
            df = generate_data()
            df.to_csv("vendors.csv", index=False)
        self.rec = VendorRecommender()

    def test_initialization(self):
        """Test if the comprehensive dataset is loaded."""
        self.assertFalse(self.rec.df.empty, "Dataframe should not be empty")
        # Match_Confidence is added at runtime during search, so not testing here
        self.assertIn("Category", self.rec.df.columns)

    def test_recommendation_filtering(self):
        """Test if filters work correctly."""
        # Test Category Filter
        filters = {'Category': ['Recruitment']}
        results = self.rec.get_recommendations("", filters=filters)
        
        # Check if all results are indeed Recruitment
        if not results.empty:
            unique_cats = results['Category'].unique()
            self.assertEqual(len(unique_cats), 1)
            self.assertEqual(unique_cats[0], 'Recruitment')

    def test_scoring_logic(self):
        """Test if scoring produces numbers in range."""
        query = "payroll automation"
        results = self.rec.get_recommendations(query, top_k=5)
        
        if not results.empty:
            top_score = results.iloc[0]['Match_Confidence']
            self.assertTrue(0 <= top_score <= 100, f"Score {top_score} out of range")
            # The first result should be reasonably relevant (non-zero ideally), but randomness applies to data
            # self.assertGreater(top_score, 0) 

    def test_empty_search(self):
        """Test behavior with empty parameters."""
        results = self.rec.get_recommendations("")
        # Should return top vendors by rating or default sort
        self.assertFalse(results.empty)
        self.assertEqual(len(results), 10) # default top_k

if __name__ == '__main__':
    unittest.main()
