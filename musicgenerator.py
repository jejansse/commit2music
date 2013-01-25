from midiutil.MidiFile import MIDIFile
import datetime
from collections import defaultdict


if __name__ == "__main__":
    authors = set()
    commits = defaultdict(list)
    last_author = ""
    for line in open("gitlogs.txt"):
        if line.startswith("Author"):
            author = line[7:-1].strip()
            authors.add(author)
            last_author = author
        elif line.startswith("Date"):
            date = datetime.datetime.strptime(line[5:-6].strip(), "%a %b %d %H:%M:%S %Y")
            if last_author:
                commits[last_author].append(date)

    author_to_note = {}
    curr_note = 60 # start with C4
    for author in authors:
        if author not in author_to_note:
            author_to_note[author] = curr_note
            curr_note += 1
    commit_date_to_authors = defaultdict(list)
    for author, commit_dates in commits.iteritems():
        for commit_date in commit_dates:
            commit_date_to_authors[commit_date.strftime("%Y-%m-%d %H:%M")].append(author_to_note[author])

    # Create a midi file with 1 track
    midi_file = MIDIFile(1)

    track = 0

    # Add track name and tempo
    midi_file.addTrackName(track,time,"Git")
    midi_file.addTempo(track,time,120)

    time = 0
    for commit_date, notes in commit_date_to_authors.iteritems():
        for note in notes:
            midi_file.addNote(0,0,note,time,1.0/8,100)
        time += 0.125

    binfile = open("git.mid", "wb")
    midi_file.writeFile(binfile)
    binfile.close()


