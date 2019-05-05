#SQL home work--04/05/2019

use sakila

#1a. Display the first and last names of all actors from the table actor.
select first_name, last_name from actor;

#1b. Display the first and last name of each actor in a single column in upper case letters.Name the column Actor Name.
select concat(first_name, ' ', last_name) as full_name from actor;

#2a. You need to find the ID number, first name, and last name of an actor, of whom you know only the first name, "Joe." What is one query would you use to obtain this information?
select actor_id, first_name, last_name from actor
	where first_name = 'Joe';

#2b. Find all actors whose last name contain the letters GEN:
select actor_id,first_name, last_name from actor
	where last_name like '%gen%';

#2c. Find all actors whose last names contain the letters LI. This time, order the rows by last name and first name, in that order:
	select actor_id, last_name, first_name from actor
		where last_name like '%li%';

#2d. Using IN, display the country_id and country columns of the following countries: Afghanistan, Bangladesh, and China:
select country_id, country from country
	where country IN ('Afghanistan','Bangladesh','China')

#3a. You want to keep a description of each actor. You don't think you will be performing queries on a description, so create a column in the table actor named description and use the data type BLOB (Make sure to research the type BLOB, as the difference between it and VARCHAR are significant).
alter table actor
add column  description BLOB after last_name;

#3b. Very quickly you realize that entering descriptions for each actor is too much effort. 
#Delete the description column.
alter table actor
drop column description;

#4a. List the last names of actors, as well as how many actors have that last name.
Select last_name, count(*) as 'Actors with same last name'
from actor group by last_name;

#4b. List last names of actors and the number of actors who have that last name, 
#but only for names that are shared by at least two actors
Select last_name, count(*) as 'Actors with same last name'
from actor group by last_name having count(*)>=2;

#4c. The actor HARPO WILLIAMS was accidentally entered in the actor table as GROUCHO WILLIAMS. 
#Write a query to fix the record.
Update actor
set first_name='Harpo'
where first_name='Groucho' and last_name='Williams';

#4d. Perhaps we were too hasty in changing GROUCHO to HARPO. It turns out that GROUCHO was the correct 
#name after all! In a single query, if the first name of the actor is currently HARPO, change it to GROUCHO.
Update actor
set first_name='Groucho'
where first_name='Harpo' and last_name='Williams';

#5a. You cannot locate the schema of the address table. Which query would you use to re-create it?

#				Hint: https://dev.mysql.com/doc/refman/5.7/en/show-create-table.html

describe address;

#6a. Use JOIN to display the first and last names, as well as the address, of each staff member. 
#Use the tables staff and address:
select first_name, last_name, address 
FROM staff s
JOIN address a
ON s.address_id=a.address_id;

#6b. Use JOIN to display the total amount rung up by each staff member in August of 2005. 
#Use tables staff and payment.
select payment.staff_id, staff.first_name, staff.last_name, payment.payment_date, payment.amount
FROM staff INNER JOIN payment ON
staff.staff_id=payment.staff_id AND payment_date LIKE '2005-08%';

#6c. List each film and the number of actors who are listed for that film. 
#Use tables film_actor and film. Use inner join.
SELECT f.title AS 'Film Title', COUNT(fa.actor_id) AS `Number of Actors`
FROM film_actor fa
INNER JOIN film f 
ON fa.film_id= f.film_id
GROUP BY f.title;

#6d. How many copies of the film Hunchback Impossible exist in the inventory system?
SELECT title, (
SELECT COUNT(*) FROM inventory
WHERE film.film_id = inventory.film_id
) AS 'Copies'
FROM film
WHERE title = "Hunchback Impossible";

#6e. Using the tables payment and customer and the JOIN command, list the total paid by each customer. 
#List the customers alphabetically by last name:
select c.first_name, c.last_name, sum(p.amount) as 'Total paid'
FROM customer c
INNER JOIN payment p
where c.customer_id=p.customer_id
GROUP BY c.customer_id
ORDER BY c.last_name;

#7a. The music of Queen and Kris Kristofferson have seen an unlikely resurgence. 
#As an unintended consequence, films starting with the letters K and Q have also soared in popularity. 
#Use subqueries to display the titles of movies starting with the letters K and Q whose language is English.
SELECT title
FROM film WHERE title 
LIKE 'K%' OR title LIKE 'Q%'
AND title IN 
(
SELECT title 
FROM film 
WHERE language_id = 1
);

#7b. Use subqueries to display all actors who appear in the film Alone Trip.
Select first_name, last_name
FROM actor
WHERE actor_id IN
(SELECT actor_id
FROM film_actor
WHERE film_id IN
(SELECT film_id
FROM film
WHERE title='Alone Trip'
));

#7c. You want to run an email marketing campaign in Canada, for which you will need the names and 
#email addresses of all Canadian customers. Use joins to retrieve this information.
SELECT cus.first_name, cus.last_name, cus.email 
FROM customer cus
JOIN address a 
ON (cus.address_id = a.address_id)
JOIN city cty
ON (cty.city_id = a.city_id)
JOIN country
ON (country.country_id = cty.country_id)
WHERE country.country= 'Canada';

#7d. Sales have been lagging among young families, and you wish to target all family movies for a promotion. 
#Identify all movies categorized as family films.

SELECT title, description FROM film 
WHERE film_id IN
(
SELECT film_id FROM film_category
WHERE category_id IN
(
SELECT category_id FROM category
WHERE name = "Family"
));

#7e. Display the most frequently rented movies in descending order.
SELECT f.title, COUNT(rental_id) AS 'Times Rented'
FROM rental r
JOIN inventory i
ON (r.inventory_id = i.inventory_id)
JOIN film f
ON (i.film_id = f.film_id)
GROUP BY f.title
ORDER BY `Times Rented` DESC;

#7f. Write a query to display how much business, in dollars, each store brought in.
SELECT s.store_id, SUM(amount) AS 'Revenue'
FROM payment p
JOIN rental r
ON (p.rental_id = r.rental_id)
JOIN inventory i
ON (i.inventory_id = r.inventory_id)
JOIN store s
ON (s.store_id = i.store_id)
GROUP BY s.store_id;

#7g. Write a query to display for each store its store ID, city, and country.
SELECT s.store_id, cty.city, country.country
FROM store s
JOIN address a
ON(a.address_id=s.address_id)
JOIN city cty
ON(cty.city_id=a.city_id)
JOIN country
ON(country.country_id=cty.country_id);

#7h. List the top five genres in gross revenue in descending order. 
#(Hint: you may need to use the following tables: category, film_category, inventory, payment, and rental.)

SELECT c.name as 'Genre', sum(p.amount) as 'Gross'
FROM category c
JOIN film_category fc
ON (c.category_id=fc.category_id)
JOIN inventory i
ON (fc.film_id=i.film_id)
JOIN rental r
ON (i.inventory_id=r.inventory_id)
JOIN payment p
ON(r.rental_id=p.rental_id)
GROUP BY c.name ORDER BY Gross LIMIT 5;


#8a. In your new role as an executive, you would like to have an easy way of viewing the 
#Top five genres by gross revenue. Use the solution from the problem above to create a view. 
#If you haven't solved 7h, you can substitute another query to create a view.

CREATE VIEW view_genre_revenue AS
SELECT c.name as 'Genre', sum(p.amount) as 'Gross'
FROM category c
JOIN film_category fc
ON (c.category_id=fc.category_id)
JOIN inventory i
ON (fc.film_id=i.film_id)
JOIN rental r
ON (i.inventory_id=r.inventory_id)
JOIN payment p
ON(r.rental_id=p.rental_id)
GROUP BY c.name ORDER BY Gross LIMIT 5;

#8b. How would you display the view that you created in 8a?
select*from view_genre_revenue;

#8c. You find that you no longer need the view top_five_genres. Write a query to delete it.
DROP VIEW view_genre_revenue;