1. **Changed the project structure:**

- **What:** Moved from single files (`models.py`, `serializers.py`, `views.py`) to a feature-based folder structure.
- **Why:** Makes the project more organized, scalable, and easier to maintain by grouping related code together.



2. **Made UUID read-only in serializers:**
- **What:** Added `read_only_fields = ['uuid']` to all serializers.
- **Why:** Prevents UUID modification and ensures it is always controlled by the system for data integrity.


3. **Fixed N+1 query problem in event list:**
- **What:** Removed per-object calculation of `total_available_tickets` from the serializer and replaced it with `annotate` in the queryset, while using `select_related("venue")` and `prefetch_related("tickettype_set")` in the view.
- **Why:** Improves performance by reducing N+1 queries and moving aggregation logic to the database, making the API faster and more efficient.


5. **Added caching with dynamic timeout based on next event:**
- **What:** Implemented caching in `EventListView` and `EventDetailsView`, using a dynamic timeout calculated from the next event start or end time.
- **Why:** Improves performance by reducing database queries while ensuring cache automatically expires when event timing changes, keeping data fresh and accurate.


6. **Added transaction safety for ticket purchasing (race condition fix):**
- **What:** Wrapped the purchase logic in `transaction.atomic()` and used `select_for_update()` on `TicketType` to lock the row during updates.
- **Why:** Prevents race conditions when multiple users try to buy tickets at the same time, ensuring accurate ticket stock and avoiding overselling.

7. **Added signals to clear cache on event and ticket changes:**
- **What:** Created signals in `signals.py` to invalidate cache when `Event` or `TicketType` is created, updated, or deleted.
- **Why:** Ensures cached data stays consistent with the database by automatically clearing stale cache whenever event or ticket information changes.

