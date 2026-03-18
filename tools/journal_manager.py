import datetime, yaml, os
from validate_label import validate_label
class JournalManager:
    def append(self, gamma, anchor="None", protocol="DETENTE"):
        entry = {'session': datetime.datetime.now().isoformat(), 'anchor': anchor, 'protocol': protocol, 'gamma': [l for l in gamma if validate_label(l).valid]}
        with open("journal.log", 'a') as f: f.write("---\n"); yaml.dump(entry, f)
        print(f"--- Journaled {len(entry['gamma'])} labels ---")
if __name__ == "__main__": JournalManager().append(["!⊕∃F+: Virtual_Environment ⊢ Tool_Isolation"], anchor="Setup")
