
## 1. What is an ODM and why do we use Beanie instead of writing raw MongoDB queries?

An ODM (Object Document Mapper) is a tool that helps us interact with a database using Python classes instead of writing raw database queries. Since MongoDB is a NoSQL database, it stores data as documents, and ODM helps map these documents to Python objects.

We use Beanie because it simplifies working with MongoDB. Instead of writing complex queries, we can use methods like `.create()`, `.find()`, or `.update()`. It also integrates well with Pydantic, which makes data validation easier and cleaner in FastAPI projects.

---

## 2. What is the role of the Database class — why wrap Beanie methods inside it instead of calling them directly in routes?

The Database class acts as a middle layer between the routes and the database. Instead of calling Beanie methods directly inside the routes, we use this class to keep the code more organized.

This makes the project cleaner and easier to maintain. If we need to change how we interact with the database later, we only need to update the Database class instead of modifying every route. It also avoids repeating the same logic in multiple places.

---

## 3. What happens if initialize_database() is not called on startup? What would break and why?

If `initialize_database()` is not called, the application will not connect to MongoDB properly. This means Beanie will not be initialized and the document models (Event and User) will not be registered.

As a result, any database operation like creating or retrieving data will fail, and the API endpoints that depend on the database will not work correctly.

---

## 4. What is the difference between the Event document and the EventUpdate model, and why are they two separate classes?

The Event document represents the full structure of an event stored in the database. All fields are required when creating a new event.

On the other hand, the EventUpdate model is used for updating existing events. Its fields are optional, which allows us to update only specific parts of an event without sending all the data again.

Keeping them separate makes the API more flexible and avoids unnecessary data requirements during update operations.

## Part B

1. I used `mongo` in `DATABASE_URL` because the FastAPI app and MongoDB run in separate Docker containers. Inside Docker Compose, containers talk to each other by service name. If I used `localhost`, the app container would try to connect to itself instead of the MongoDB container, so the connection would fail.

2. `depends_on` makes Docker start the mongo service before the app service. During testing, I noticed that this only controls start order, not full readiness. MongoDB may still need a moment before accepting connections. A health check would be a more reliable way to wait until the database is fully ready.

3. The volume in the mongo service keeps database files outside the container. I tested this by creating data, stopping the containers, and starting them again. The data was still there, which showed that persistence was working. Without the volume, the data would be lost when the container is removed.

4. In the Dockerfile, `requirements.txt` is copied before the rest of the app so Docker can cache dependency installation. This makes rebuilds faster because if only the app code changes, Docker does not need to reinstall all packages again.