class Presets():
    def __init__(self) -> None:
        pass

    @staticmethod
    def get_table_example():
        return """
        {
                "exercises": [
                    {
                    "exercise": "Barbell Bench Press",
                    "sets": 4,
                    "reps": 8,
                    "rest_time_seconds": 90
                    },
                    {
                    "exercise": "Overhead Dumbbell Press",
                    "sets": 3,
                    "reps": 10,
                    "rest_time_seconds": 60
                    },
                    {
                    "exercise": "Incline Dumbbell Fly",
                    "sets": 3,
                    "reps": 12,
                    "rest_time_seconds": 60
                    },
                    {
                    "exercise": "Tricep Dips",
                    "sets": 3,
                    "reps": 10,
                    "rest_time_seconds": 90
                    },
                    {
                    "exercise": "Push-Ups",
                    "sets": 3,
                    "reps": 15,
                    "rest_time_seconds": 60
                    }
                ]
            }"""