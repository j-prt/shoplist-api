# ShopList API (WIP)

RESTful API for creating and managing shopping lists using Django REST Framework.

## Overview

The inspiration for this project is an issue I've long had: managing my shopping lists. Every time I remember I have to buy something I make a note in my phone, on a postit, on my hand, on an index card.. etc. When it comes time to actually do my shop, I find that I'm scraping together all this data and trying to make a coherent list of what I need to buy, and where. And I have no idea how much it will cost. 

## The API

This is a RESTful API. CRUD (Create, Read, Update, Delete) operations can be performed on most endpoints and allow for creating and managing a shopping list. Python is version 3.9 running on a Docker Alpine (Linux). The DB is a Docker PostgreSQL instance as well. Web framework is Django REST Framework, API documentation is with Swagger via [DRF-Spectacular](https://drf-spectacular.readthedocs.io/en/latest/).

View the live API documentation (interactive) [here](http://ec2-54-221-108-20.compute-1.amazonaws.com/api/docs/).

## Model design

The API comprises five models: User, ShopList, Item, Store, and Category. 

### User
- ForeignKey in all other DB tables
- API provides account creation and token-based authentication 

### ShopList
- Model for storing lists. ManyToMany relationship with Item. Custom total field to reflect the total cost of the items in the list.
- API provides:
  - Creating a new list
  - Replacing an existing list (PUT)
  - Partially updating an existing list (PATCH)
  - Adding Item objects to the list via custom endpoint (POST)
  - Deletion (DELETE)
  
### Item
- Model for storing item information. ManyToMany relationships with ShopList, Category, and Store.
- API provides:
  - Replacing existing items (PUT).
  - Partially updating an existing item (PATCH)
  - Deletion (DELETE)
  
### Store
- Model for designating the store(s) where an item can be found.
- API provides:
  - Replacing existing items (PUT).
  - Partially updating an existing item (PATCH)
  - Deletion (DELETE)
  
### Category
- Model for designating the category(ies) each item belongs to.
- API provides:
  - Replacing existing items (PUT).
  - Partially updating an existing item (PATCH)
  - Deletion (DELETE)
  
  
 ## Tools
 - [Django](https://www.djangoproject.com/)
 - [Django REST Framework](https://www.django-rest-framework.org/)
 - [DRF-Spectacular](https://drf-spectacular.readthedocs.io/en/latest/)
 - [Docker](https://www.docker.com/)
 - [PostgreSQL](https://www.postgresql.org/)
 - [Amazon Web Services EC2](https://aws.amazon.com/ec2/)
 
