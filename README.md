# ReceiptAPI
Backend API platform for managing family receipt

Not sure if it is a good ideal to integrate the following ideals into one app. But I'll list my thoughts here as a record.
TODO: Events management like diary, funny stories happened in the family.
TODO: Cloud storage for family use.

## App breakdown
Scenario: Upload a recipe for OCR -> extract text from image -> process text as data stream -> input into database

App features:
    - user authentication/authorization  
    - upload images (multipart box)  
    - image OCR (ML engine using trained model)  
      - for image  
      - for pdf (TODO): pdf from bank statement, logic for this part is completely different from receipts  
    - process text  
      - OCR output is a list of extracted text  
      - need to process text accordingly  
        - factory design pattern  
        - user interface: get_image, run_ocr, process_orc_text, write_to_database  
        - may need to write a class for each store for text processing  
    - user data visualization  
      - family spend/earn total  
        - per day/month/year  
      - user spend/earn total  
        - per day/month/year  
    - view receipts  
      - list all receipts for current user  
      - may need pagination  

Services:  
    - user login/sign up  
    - image OCR  
    - data aggregation/visualization  

Storage:  
    - For developing: sqlite should be enough  
    - For deployment:
      - IAM for account management
      - EC2 for running app image
      - AWS S3 for image storage
      - RDS for database

Data Models:
    - users
      - login/logout, sign up, delete
      - Properties: username, password
    - receipts:
      - each piece of payment receipts is a receipts object
      - Properties: id, store, time, user, items, total, image_id
    - items:
      - an item on the receipt
      - Properties: id, name, description, receipt

Utility functions:
    - OCR
      - run_ocr
      - process_ocr_text
      - receipt/item_serializer
    - Data visualization
      - compute total spend/earn per request

## Things to finish to get started

Environment setup
    - Github repo
    - Docker developing env
      - docker file
      - docker compose file
      - requirements.txt
