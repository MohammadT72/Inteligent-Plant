# main.py
from functions.general import AudioProcessor
from API import OPENAI_API_KEY
# Constants


# Sentences to process
sentences = [
    "Goodbye...My lovely friend...see you later!",
    "Are you talking to me!!!?..........Are you talking to me!!!?..... Just kidding, Robert De Niro style,....love it!?,.........checking the plant status....Pleas wait",
    "Houston,......Houston......we have a problem......with a leaf!..... Fixing it right away.",
    "I'll be back... just pruning this plant!.....",
    "Why.....so....serious?.....Ha ha ha...I'm just adjusting the soil pH.....One moment!",
    "May the force be with you........while I water the plants.....",
    "I'm gonna make this plant healthy...an offer it can't refuse.....",
    "Life.....is like a box of chocolates... and this plant....needs some TLC..... Be right back!",
    "Say hello.......to my little friend...the watering can!..... Hold tight.",
    "You're gonna need a bigger pot..... Just a moment, making the switch!",
    "To infinity and beyond!..... Or at least to the next plant check-up..... One sec.",
    "You can't handle the truth... but this plant needs a trim..... Almost done!",
    "Here's looking at you, kid... while I adjust the sunlight..... Hang on!",
    "Frankly, my dear, I do give a leaf... Fixing it right now!.....",
    "Hmmm......I've got a feeling we're not in Kansas anymore... Oh wait, just checking the humidity.....",
    "You talking to me?..... Just making sure this plant is talking too..... Be right back!",
    "E.T. phone home... while I check on the roots..... One moment!",
    "I see dead plants... Just kidding, they're all alive!..... Just adjusting one thing.",
    "Go ahead, make my day... and wait a moment while I fix this.....",
    "I am Groot... Just doing some plant maintenance..... Hang tight!",
    "The name's Bond, Plant Bond... and I'm on a mission to keep things green..... Be right back!",
    "Oops, it looks like a leaf fell off... Let me pick that up..... Just a moment!",
    "Hang on, I'm watering the plants..... This will just take a few seconds.",
    "Hmm, I think a root needs adjusting..... I'll be right back!",
    "Hold on, I see a weed... Let me pull that out quickly.....",
    "Uh-oh, a branch is out of place... I'll fix it right away!.....",
    "Just a moment, I'm pruning some leaves..... Almost done!",
    "Oh dear, it seems the soil is a bit dry..... Adding some water now.",
    "Hmmm, I'm checking the sunlight levels..... Be right with you!",
    "Aha, I found a pest..... Removing it promptly..... Please wait.",
    "Just a sec, I'm adjusting the fertilizer..... Nearly finished!",
    "Hmm, a plant needs a bit of support..... Let me handle that.",
    "One moment, I'm arranging the flowers..... Won't be long!",
    "Oops, a pot is tipped over... I'll fix it immediately.....",
    "Hold tight, I'm checking the humidity..... Almost there!",
    "Hmmm, a plant is growing sideways..... I'll straighten it up.",
    "Oh, there's a bit of dust on the leaves..... Let me clean that.",
    "Hang on, I'm adjusting the plant's position for better light..... Just a bit longer!",
    "Hmm, I'm checking the plant's health..... Be right with you.",
    "Aha, a new leaf is sprouting..... Let me ensure it's safe.",
    "Oops,....some petals... have fallen..... Cleaning up right now."
]

def main():
    audio_processor = AudioProcessor(OPENAI_API_KEY)
    
    for index, text in enumerate(sentences[:2]):
        output_filename = f'audio_{index}.wav'
        output_filename = audio_processor.text_to_speech_to_file(text, output_filename=output_filename)
        print(f"Audio file saved as: {output_filename} (Sentence {index + 1})")

if __name__ == "__main__":
    main()
