from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Products, Order
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd





class RecommendationView(APIView):

    def get(self, request, user_id):
        # user_id = id
        print(user_id, 'user id...')

        if not user_id:
            print(user_id, 'id')
            return Response({"error": "User ID is required"}, status=400)

        # Get user's order history
        user_orders = Order.objects.filter(user=user_id)

        user_products = set()
        for order in user_orders:
            print(len(user_orders), 'user orders....')

            for item in order.items:
                print(item, 'orders...')
                user_products.add(item['product'])

        # Get all products
        all_products = Products.objects.all()

        print(len(Products.objects.all()), 'all')
        # Create a DataFrame for content-based filtering
        df = pd.DataFrame(list(all_products.values()))
        print(list(all_products.values()),'tes....')
        df['content'] = df['productName'] + ' ' + df['category'] + ' ' + df['description']

        # TF-IDF Vectorization
        tfidf = TfidfVectorizer(stop_words='english')
        tfidf_matrix = tfidf.fit_transform(df['content'])

        # Compute cosine similarity
        cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

        # Get indices of products the user has ordered
        user_product_indices = df[df['_id'].isin(user_products)].index

        # Get similar products
        similar_products = []
        for idx in user_product_indices:
            sim_scores = list(enumerate(cosine_sim[idx]))
            sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
            sim_scores = sim_scores[1:6]  # Top 5 similar products
            similar_products.extend([i[0] for i in sim_scores])

        # Remove duplicates and products the user has already ordered
        recommended_products = list(set(similar_products) - set(user_product_indices))

        # Get the recommended product details
        recommendations = df.iloc[recommended_products][['_id', 'productName', 'category', 'price']].to_dict('records')

        return Response(recommendations)