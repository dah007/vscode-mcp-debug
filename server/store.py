# Simple in-memory store
# Structure: List of debug sessions with all their events
debug_sessions = []
current_session = None

# Also maintain the old structure for backward compatibility
debug_data = {
    "variables": {},
    "stack": [],
    "breakpoints": [],
    "sessions": []
}
