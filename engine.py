import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class VendorRecommender:
    def __init__(self, data_path="vendors.csv"):
        """
        Initialize the advanced recommender system.
        """
        try:
            self.df = pd.read_csv(data_path)
            self.df['Description'] = self.df['Description'].fillna('')
            self._prepare_vectors()
            print("VendorMatch AI Engine initialized.")
        except FileNotFoundError:
            print(f"Error: {data_path} not found. Please run data_gen.py first.")
            self.df = pd.DataFrame()
            self.tfidf_matrix = None

    def _prepare_vectors(self):
        """
        Vectorize descriptions using TF-IDF with English stop words.
        """
        self.vectorizer = TfidfVectorizer(stop_words='english')
        self.tfidf_matrix = self.vectorizer.fit_transform(self.df['Description'])

    def get_recommendations(self, query, filters=None, top_k=10):
        """
        Get recommendations based on query and filters.
        
        Args:
            query (str): User's natural language query.
            filters (dict): Dictionary of filters e.g. {'Category': [], 'Cost_Tier': []}.
            top_k (int): Number of results to return.
            
        Returns:
            pd.DataFrame: Recommended vendors with 'Match_Confidence'.
        """
        if self.df.empty:
            return pd.DataFrame()

        # 1. Filter Data First (Optional strategy: Filter then score, or Score then filter. 
        # For performance on large datasets, Filter then Score is better. 
        # But here we need to maintain index alignment with tfidf_matrix if we filter first.
        # Easiest approach for medium data: Score ALL, then filter results.)
        
        # Calculate scores
        if query and query.strip():
            query_vec = self.vectorizer.transform([query])
            similarity_scores = cosine_similarity(query_vec, self.tfidf_matrix).flatten()
            self.df['Match_Confidence'] = (similarity_scores * 100).round(1)
        else:
            # If no query, return 0 confidence, just list filtered
            self.df['Match_Confidence'] = 0.0

        # Create a working copy
        results = self.df.copy()

        # 2. Apply Filters
        if filters:
            if 'Category' in filters and filters['Category']:
                results = results[results['Category'].isin(filters['Category'])]
            
            if 'Cost_Tier' in filters and filters['Cost_Tier']:
                results = results[results['Cost_Tier'].isin(filters['Cost_Tier'])]
                
            if 'Min_Rating' in filters and filters['Min_Rating']:
                results = results[results['Rating'] >= filters['Min_Rating']]

        # 3. Sort and Return
        if query and query.strip():
            results = results.sort_values(by='Match_Confidence', ascending=False)
        else:
            # If no query, maybe sort by Rating
            results = results.sort_values(by='Rating', ascending=False)
            
        return results.head(top_k)

    def get_analytics_data(self):
        """
        Return data for analytics dashboard.
        """
        return self.df

if __name__ == "__main__":
    # Test
    rec = VendorRecommender()
    if not rec.df.empty:
        print("Testing Recommendation...")
        res = rec.get_recommendations("recruitment for tech startups", filters={'Cost_Tier': ['Medium', 'High']})
        print(res[['Name', 'Category', 'Cost_Tier', 'Match_Confidence']].head())
