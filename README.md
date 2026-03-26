# Book Search System using AVL Tree

## Overview

This project implements a self-balancing AVL Tree to search over 10,000 book records from the Goodreads dataset.

The goal is to compare how well AVL performs over Linear Search on Large Datasets.

The system allows users to search for a Title of the book in a search bar and find the details of the book such as Author of the Book, The Year it was published, Number of pages, Ratings for the book.

Example:

Input: Enter Book Title to Search (or 'exit'): A Little Princess

Output: MATCH FOUND:

• Title: A Little Princess  
• Author: Frances Hodgson Burnett/Nancy Bond  
• Year: 2002 | Pages: 242 | Rating: 4.2  

---

## Dataset

The project uses Goodreads Books Dataset, which contains more than 11,000 records.

Source: https://www.kaggle.com/datasets/jealousleopard/goodreadsbooks

Each book includes several metadata fields:

1. Book Title (Primary Key)  
2. Author Name  
3. Average Rating  
4. Number of Pages  
5. Publication Date  

Since this is a real world data, it will contain noise such as:

1. Column names like ‘  num_pages’ had accidental leading spaces.  
2. Dates were strings (MM/DD/YYYY) rather than simple years.  
3. Some books had empty fields for ratings or page counts.  

---

## Preprocessing

Before building the tree, the dataset will undergo a cleaning pipeline to handle the noise:

1. Removes the accidental spaces from column names.  
2. Converts the text-based page counts and ratings into numbers, replacing errors with zeros to prevent crashes.  
3. Transforms complex date strings (9/16/2006) into a simple integer (2006).  
4. Removes any book records that are missing a title.  

---

## Algorithm Used

The main algorithm used is an AVL Tree.

An AVL Tree is a binary search tree that self-balances. Every time a book is added, the tree checks if one side is getting too heavy. If it is, then it performs Rotations (Left, Right, or a combination) to stay perfectly symmetrical.

Why use an AVL Tree?

Standard Search: Looks through every book one-by-one with O(N) time.

AVL Search: Because the tree is balanced, it will cut the search area into half with every step (O(logN) time).

Result: In a list of 11,000 books, a standard search might take 11,000 steps, while the AVL tree finds it in at most 14 steps.

---

## Features

1. Finds any book in a 11,000+ record database in microseconds.  
2. Automatically maintains its own efficiency using tree rotations.  
3. Returns Author, Pages, Rating, and Year in a clean format.  
4. Shows a side-by-side time comparison between the AVL Tree and a Linear Search.  

---

## Project Structure

book_search.py → Main application (Cleans data, builds tree, and runs search).  
books.csv → The raw Goodreads dataset.  
cleaned_books.csv → The file created after the preprocessing step.  
README.md → Instructions and project documentation.  
MSML606_Project_Proposal.pdf → The project plan.  

---

## How to Run

Install dependency: pip install pandas  

Run program: python book_search.py  

---

## Key Learning Outcomes

1. Building and balancing an AVL Tree from scratch.  
2. Solving "noise" issues like hidden spaces and inconsistent date formats.  
3. Proving that O(logN) is significantly faster than O(N) for large datasets.  
4. Successfully storing and retrieving complex objects within tree nodes.  

---

## Conclusion

This project demonstrates that an AVL Tree is an effective way to manage large scale search systems.

AVL Tree is far more efficient than Linear search for larger Datasets.

---

## AI Usage Statement

I used AI for guidance during development. I used AI to understand the search interface and the logic to run the loop indefinitely until the user types exit, and handle keyboard interruptions and exceptions.

No AI Used for Core Logic. All the core logic, Tree implementation, data preprocessing logic for handling noisy data and data access logic is done manually by me.

The Documentation in Code, Comments, READ ME are manually authored.
