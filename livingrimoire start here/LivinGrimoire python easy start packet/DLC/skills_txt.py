import os
from datetime import date, datetime
from LivinGrimoirePacket.LivinGrimoire import Skill


class DiMovieEvents(Skill):
    """
    Movie release tracker skill.

    Add a movie at runtime:
        "upcoming movie <title> <DDMMYY>"
        e.g. "upcoming movie C++: The Documentary 040626"

    Bulk-load from DLC/movies.txt (one entry per line):
        <title> <DDMMYY>
        e.g.  C++: The Documentary 040626

    Get an update:
        ear contains "movies update"
        → replies one sentence per movie, describing how far away each is.

    Expiry:
        Movies more than 30 days past their release date are silently dropped.
    """

    _MOVIES_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "movies.txt")

    def __init__(self):
        super().__init__()
        self._movies: dict[str, date] = {}

    # --------------------------------------------------------------- manifest

    def manifest(self):
        """
        Ensures movies.txt exists, then loads it.
        """
        # Create the file if missing
        if not os.path.exists(self._MOVIES_FILE):
            with open(self._MOVIES_FILE, "w", encoding="utf-8") as f:
                pass  # create empty file

        self._load_from_file()

    # --------------------------------------------------------------- load/save

    def _load_from_file(self):
        """
        Loads movies from movies.txt into memory.
        Format: <title> <DDMMYY>
        """
        self._movies.clear()

        try:
            with open(self._MOVIES_FILE, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue

                    # split only on last space
                    parts = line.rsplit(" ", 1)
                    if len(parts) != 2:
                        continue

                    title, date_token = parts
                    try:
                        release = datetime.strptime(date_token, "%d%m%y").date()
                        self._movies[title] = release
                    except ValueError:
                        continue
        except FileNotFoundError:
            # Should never happen because manifest() creates the file
            pass

    def _save_to_file(self):
        """
        Writes current movies to movies.txt.
        """
        with open(self._MOVIES_FILE, "w", encoding="utf-8") as f:
            for title, release in self._movies.items():
                f.write(f"{title} {release.strftime('%d%m%y')}\n")

    # ------------------------------------------------------------------ input

    def input(self, ear: str, skin: str, eye: str):
        ear_stripped = ear.strip()
        lower = ear_stripped.lower()

        if lower.startswith("upcoming movie "):
            self._handle_add(ear_stripped)
        elif any(t in lower for t in ("movies update", "upcoming movies", "what movies", "movie update")):
            self._handle_update()

    # ------------------------------------------------------------------ add

    def _handle_add(self, ear: str):
        parts = ear.split()
        if len(parts) < 4:
            self.setVerbatimAlg(4, "I need a title and a date — e.g. 'upcoming movie Dune 3 041226'.")
            return

        date_token = parts[-1]
        if len(date_token) != 6 or not date_token.isdigit():
            self.setVerbatimAlg(4, "Date should be 6 digits in DDMMYY format, e.g. 040626.")
            return

        title = " ".join(parts[2:-1])

        try:
            release = datetime.strptime(date_token, "%d%m%y").date()
        except ValueError:
            self.setVerbatimAlg(4, f"Couldn't parse that date: {date_token}. Use DDMMYY format.")
            return

        if (date.today() - release).days > 30:
            self.setVerbatimAlg(4, f"{title} came out over a month ago — not adding it.")
            return

        self._movies[title] = release
        self._save_to_file()

        self.setVerbatimAlg(4, f"Got it, added {title} releasing on {release.strftime('%d %b %Y')}.")

    # ------------------------------------------------------------------ update

    def _handle_update(self):
        today = date.today()

        # Drop expired movies
        self._movies = {
            t: d for t, d in self._movies.items()
            if (today - d).days <= 30
        }

        self._save_to_file()

        if not self._movies:
            self.setVerbatimAlg(4, "No upcoming movies on the list right now.")
            return

        lines = []
        for title, release in sorted(self._movies.items(), key=lambda x: x[1]):
            lines.append(self._describe(title, release, today))

        self.setVerbatimAlg(4, *lines)

    # ------------------------------------------------------------------ time description

    def _describe(self, title: str, release: date, today: date) -> str:
        delta = (release - today).days

        if delta > 1:
            return f"{title} releases in {delta} days."
        elif delta == 1:
            return f"{title} releases tomorrow."
        elif delta == 0:
            return f"{title} releases today."
        else:
            return f"{title} released {-delta} days ago."