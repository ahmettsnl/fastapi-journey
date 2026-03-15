# DECISIONS

## Why did you choose each Pydantic field type?

I used integer for id and age because they represent numeric values.
String was used for name and email because they represent text.
Appointment is a nested model inside Patient to represent the relationship between patients and their appointments.

## What does each validation rule protect against?

The age field has constraints (gt=0, lt=120) to prevent invalid ages.
The name field has min_length and max_length to avoid empty or extremely long names.
Doctor and reason fields also have length validations to ensure meaningful input.

## Which endpoint uses async in a meaningful way?

The GET /patients endpoint uses async and includes await asyncio.sleep(1).
This simulates a delay similar to a real database query in a real-world application.