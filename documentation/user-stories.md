# User stories

The SQL provided is not the exactly same that SQLAlchemy generates, but it's supposed to give the reader some understanding of the underlying database structure.

## User management
- [x] **User can register**
- [x] **User can login**
- [x] **User can logout**

## Category management
- [x] **User can create a new category**
- [x] **User can view a category**
- [x] **User can list categories**
- [x] **User can delete a category**
- [x] **User can modify a category**
- [x] **User can add a bookmark to a category**
- [x] **User can remove bookmark from a category**
- [x] **User can not see or change other users' categories**
- [x] **User can add categories as child categories**
- [x] **User can not create a category with an existing name**
- [x] **User can view child categories of a category**

```
SELECT * FROM Category
JOIN CategoryInheritances ON CategoryInheritance.child_id = Category.id
where CategoryInheritance.parent_id = ?
```

- [x] **User can remove child categories from a category**
- [x] **User has to confirm when deleting a category**

# Category listing
- [x] **User can see count of bookmarks in a category**

```
SELECT COUNT(Category.id)
FROM Category
JOIN CategoryBookmark ON Category.id = CategoryBookmark.category_id
WHERE Category.id = ?
GROUP BY Category.id
```

- [x] **User can see count of child categories in a category**

```
SELECT COUNT(Category.id)
FROM Category
JOIN CategoryInheritance ON CategoryInheritance.parent_id = Category.id
WHERE Category.id = ?
```

- [x] **User can see count of parent categories for a category**

```
SELECT COUNT(Category.id)
FROM Category
JOIN CategoryInheritance ON CategoryInheritance.parent_id = Category.id
WHERE CategoryInheritance.parent_id = ?
```

## Bookmark management
- [x] **User can create a new bookmark**
- [x] **User can delete a bookmark**
- [x] **User can list bookmarks**
- [x] **User can edit an existing bookmark**
- [x] **User can add category to a bookmark**
- [x] **User can remove category from a bookmark**
- [x] **User can not see or change other users' bookmarks**
- [x] **User can not create a bookmark with an existing link or text**

## Bookmark listing
- [x] **User can see count of categories the bookmark belongs in**

```
SELECT COUNT(Bookmark.id)
FROM Bookmark
JOIN CategoryBookmark ON Bookmark.id = CategoryBookmark.bookmark_id
wHERE Bookmark.id = ?
```

- [x] **User can list uncategorized bookmarks**

```
SELECT * FROM Bookmark
WHERE Bookmark.user_id = ?
AND Bookmark.id NOT IN (
    SELECT bookmark_id FROM CategoryBookmark
)
```

- [x] **User can list bookmarks in a category**

```
SELECT * FROM Bookmark
JOIN CategoryBookmark ON CategoryBookmark.category_id = Bookmark.id
WHERE CategoryBookmark.category_id = ?
```

- [x] **User can list bookmarks in a category and all its child categories**

So this is the only query not written using SQLAlchemy. It's doable in SQLAlchemy, but because of time constraints, I just decided to use the plain SQL version.

To query for the tree hierarchy of parent-child relationships amongst categories the following query is used:

```
WITH RECURSIVE children (parent_id, child_id) AS (
    SELECT parent_id, child_id
    FROM categoryinheritance WHERE parent_id = :category_id
UNION
    SELECT ci.parent_id, ci.child_id
    FROM categoryinheritance ci
    JOIN children c ON ci.parent_id = c.child_id
)
SELECT child_id FROM children
```

- [x] **User can list bookmarks so that the bookmarks belong to all the categories she has selected**

This is probably the most complex (and slowest) of all queries.

When looking for bookmarks that belongs in all selected categories, we also need to look in to the category hierarchy.

So the query is built like this: If selected categories have ids 2, 5, 8, then first we query for the tree hierarchy for the categories in question.

Let's say category 2 has children 21, 22, 23. Category 5 has children 51, 58, 61. And Category 8 has children 14, 88, 95.

Then we build query:

```
SELECT Bookmark.id
FROM CategoryBookmark
WHERE Category.id IN (2, 21, 22, 23)

INTERSEECT

SELECT Bookmark.id
FROM CategoryBookmark
WHERE Category.id IN (5, 51, 58, 61)

INTERSEECT

SELECT Bookmark.id
FROM CategoryBookmark
WHERE Category.id IN (8, 14, 88, 61)
```

So basically all the bookmarks in the tree hierarchies are selected and then interseected to find out the bookmark ids that are _all_ in the wanted categories.

After figuring out these `bookmark_ids` it just matter of simply query to get the bookmarks out of them.

```
SELECT * FROM Bookmark WHERE Bookmark.id IN (bookmark_ids)
```

## Admin
- [x] **Admin can list users**
- [x] **Admin can delete a user**
