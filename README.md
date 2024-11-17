Installation
To run this project locally, follow these steps:

Clone the repository:

```
git clone https://github.com/mamula2023/fruitables_clone.git
```

Navigate to the project directory
```
cd fruitables_clone
```


Install dependencies:
```
pip install -r requirements.txt
```

Run the application:
```
python manage.py runserver [port]
```


Features:
User can browse products on website. Website has functionality to filter products by category, max price or tags.
There is functionaly pagination with 10 items per page (there is not 10 items in database in total :(   ), which can be changed in store/views.py
User can add products to Cart. Currently there is no 'users' on website, so every Add to Cart action results in add items to one unique cart.
If there is no such product in cart, it adds product.min_weight in quantity and every other click to Add to Cart results in increasing quantity by 1.

Not implemented: Search functionality.


test append
