-- C.a

INSERT INTO Category (mainCategory, subCategory, catNotes)
VALUES ('furniture', 'sofa', 'sofa furnitures'),
       ('furniture', 'lighting', 'stuff that lets you see'),
       ("furniture", "chair", "things you sit on"),
       ("artwork", "oil painting", "stuff to look at")

INSERT INTO Item (iDescription, photo, color, isNew, hasPieces, material, mainCategory, subCategory)
VALUES ('two-piece yellow sofa', NULL, 'yellow', TRUE, TRUE, 'silk', 'furniture', 'sofa'),
       ('blue desk lamp', NULL, 'blue', FALSE, FALSE, 'steel', 'furniture', 'lighting'),
       ("green dining set", NULL, "green", TRUE, TRUE, "wood", "furniture", "chair");

INSERT INTO Person (userName, password, fname, lname, email)
VALUES ('testUser123', 'passwd', 'test', 'User', 'testUser123@example.com'),
       ('janedoe', 'passwd', 'jane', 'doe', 'jd@nyu.edu'),
       ('bobsmith', 'passwd', 'bob', 'smith', 'bs@nyu.edu'),
       ('yourname', 'passwd', 'your', 'name', 'yn@nyu.edu');

INSERT INTO Role (roleID, rDescription)
VALUES (1, 'staff'),
       (2, 'volunteer'),
       (3, 'donor'),
       (4, 'administrator'),
       (5, 'client');

INSERT INTO Act (userName, roleID)
VALUES ('testUser123', 3),
       ('janedoe', 5),
       ('bobsmith', 1),
       ('yourname', 2);

INSERT INTO DonatedBy (ItemID, userName, donateDate)
VALUES (1, 'testUser123', CURDATE());

INSERT INTO Location (roomNum, shelfNum, shelf, shelfDescription)
VALUES (5, 0, NULL, "test shelf"),
       (2, 1, NULL, "lamps shelf"),
       (10, 230, NULL, "chairs shelf");

INSERT INTO Piece (ItemID, pieceNum, pDescription, length, width, height, roomNum, shelfNum, pNotes)
VALUES (1, 1, 'sofa body', 30, 20, 20, 5, 0, 'Stored in Room 5, no designated shelf'),
       (1, 2, 'cushion', 5, 5, 5, 5, 0, 'Stored in Room 5, no designated shelf'),
       (2, 1, 'lamp', 0.5, 0.4, 2, 2, 1, 'Only one piece'),
       (3, 1, "green dining chair", 24.2, 26, 26, 10, 230,  "one of four"),
       (3, 2, "green dining chair", 24.2, 26, 26, 10, 230,  "one of four"),
       (3, 3, "green dining chair", 24.2, 26, 26, 10, 230,  "one of four"),
       (3, 4,  "green dining chair", 24.2, 26, 26, 10, 230, "one of four - has a small scratch");

INSERT INTO Ordered (orderID, orderDate, orderNotes, supervisor, client)
VALUES (12345, '2024-01-01', "no notes", "bobsmith", "janedoe"),
       (11111, '2022-12-23', "yourname is a volunteer", "bobsmith", "yourname");

INSERT INTO ItemIn (ItemID, orderID, found)
VALUES (3, 12345, FALSE),
       (1, 11111, TRUE),
       (2, 11111, TRUE);






