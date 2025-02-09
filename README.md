# How to run

1. Install venv

```bash
  source venv/bin/activate
  python -m venv venv
  pip install -r requirements.txt
```

2. Generate data for missing functions
https://warcraft.wiki.gg/wiki/World_of_Warcraft_API/Classic

Look at the list
Vanilla & Cataclysm to find the missing functions such as "AbandonQuest" which is not under C_QuestLog
I just copied the list through HTML and created the list in 

It will read the lookup.json file, if you add more functions you need to regenerate the lookup.json file

```bash
  python Classic-API-Generator.py
```
This will then run through the lookup.json file and generate the missing functions using OpenAI


3. init_Clonerepos.sh

```bash
  bash init_Clonerepos.sh
```

4. Generate data from the cloned repositories

```bash
  python WoWUI-generator.py --version Classic
```