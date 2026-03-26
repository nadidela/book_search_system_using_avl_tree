

import pandas as pd
import csv
import time

# Data Preprocessing
def preprocess(input_csv):
    print("DATA PREPROCESSING")

    # Loading the Data
    df = pd.read_csv(input_csv, on_bad_lines='skip')
    print(f"\nSTEP 1 Raw Data Loaded: Found {len(df)} initial records.")
    print("Sample Before Cleaning:")
    print(df[['title', '  num_pages', 'publication_date']].head(2))

    # 1. Removing leading spaces from coloumns

    df.columns = [col.strip() for col in df.columns]

    # 2. Numeric Conversion

    df['num_pages'] = pd.to_numeric(df['num_pages'], errors='coerce').fillna(0).astype(int)
    df['average_rating'] = pd.to_numeric(df['average_rating'], errors='coerce').fillna(0.0)

    # 3. Transforming complex Data strings into integers
    def extract_year(date_str):
        try:
            return int(str(date_str).split('/')[-1])
        except (ValueError, IndexError):
            return 0
    df['publication_year'] = df['publication_date'].apply(extract_year)

    # 4. Record Cleaning
    df = df.dropna(subset=['title'])
    df['title'] = df['title'].str.strip()

    # Selecting final metadata fields
    cleaned_df = df[['title', 'authors', 'publication_year', 'num_pages', 'average_rating']]

    print("\nPreprocessing Complete.")
    print("Sample After Cleaning:")
    print(cleaned_df.head(2))

    cleaned_df.to_csv('cleaned_books.csv', index=False)
    print(f"Total Records ready for AVL Tree: {len(cleaned_df)}")
    return 'cleaned_books.csv'

# AVL TREE IMPLEMENTATION
class BookNode:
    def __init__(self, title, author, year, pages, rating):
        self.title = title
        self.author = author
        self.year = year
        self.pages = pages
        self.rating = rating
        self.left = None
        self.right = None
        self.height = 1

class AVLTree:
    def get_height(self, node):
        return node.height if node else 0

    def get_balance(self, node):
        return self.get_height(node.left) - self.get_height(node.right) if node else 0

    def rotate_right(self, y):
        x = y.left
        T2 = x.right
        x.right = y
        y.left = T2
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        x.height = 1 + max(self.get_height(x.left), self.get_height(x.right))
        return x

    def rotate_left(self, x):
        y = x.right
        T2 = y.left
        y.left = x
        x.right = T2
        x.height = 1 + max(self.get_height(x.left), self.get_height(x.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        return y

    def insert(self, root, data):
        if not root:
            return BookNode(*data)

        if data[0] < root.title:
            root.left = self.insert(root.left, data)
        elif data[0] > root.title:
            root.right = self.insert(root.right, data)
        else:
            return root # Skiping the duplicate titles

        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))
        balance = self.get_balance(root)

        # Balancing Logic for Self-Balancing Rotations
        if balance > 1 and data[0] < root.left.title:
            return self.rotate_right(root)
        if balance < -1 and data[0] > root.right.title:
            return self.rotate_left(root)
        if balance > 1 and data[0] > root.left.title:
            root.left = self.rotate_left(root.left)
            return self.rotate_right(root)
        if balance < -1 and data[0] < root.right.title:
            root.right = self.rotate_right(root.right)
            return self.rotate_left(root)

        return root

    def search(self, root, title):
        if not root:
            return None
        if root.title.lower() == title.lower():
            return root
        if title.lower() < root.title.lower():
            return self.search(root.left, title)
        return self.search(root.right, title)

# SEARCH INTERFACE
def run_project():
    # Preprocess
    clean_file = preprocess('books.csv')

    # Initializing the structures
    tree = AVLTree()
    root = None
    linear_data = []

    print("\nBUILDING AVL TREE")
    with open(clean_file, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            book_info = (row['title'], row['authors'], row['publication_year'],
                         row['num_pages'], row['average_rating'])
            root = tree.insert(root, book_info)
            linear_data.append(book_info)

    print("\nBook Search System")
    # This loop will run indefinitely until user types 'exit'.
    while True:
        try:
            print("\n" + "="*45)
            query = input("Enter Book Title to Search (or 'exit'): ").strip()

            if not query:
                continue
            if query.lower() == 'exit':
                print("Exiting application...")
                break

            # AVL Search Efficiency O(log n)
            start_avl = time.perf_counter()
            res_avl = tree.search(root, query)
            end_avl = time.perf_counter()

            # Linear Search Baseline Comparison O(n)
            start_lin = time.perf_counter()
            res_lin = next((b for b in linear_data if b[0].lower() == query.lower()), None)
            end_lin = time.perf_counter()

            if res_avl:
                print(f"\nMATCH FOUND:")
                print(f"• Title:  {res_avl.title}")
                print(f"• Author: {res_avl.author}")
                print(f"• Year:   {res_avl.year} | Pages: {res_avl.pages} | Rating: {res_avl.rating}")
            else:
                print(f"\nResult: No record found for '{query}'.")

            print(f"\nPERFORMANCE EVALUATION")
            print(f"AVL Tree Time: {end_avl - start_avl:.10f}s")
            print(f"Linear Search Time: {end_lin - start_lin:.10f}s")

        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"An error occurred: {e}. Returning to search...")

if __name__ == "__main__":
    run_project()
