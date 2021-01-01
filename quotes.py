import json
import re
import csv

'''
discord message format
{
  messages: [
    "timestamp": "2019-12-31T06:57:05.326+00:00",
    "content": "Chris: No. You want to be very stimulated",
    "author": {
      "name": "Audux",
      }
    
  ]
}

Reports
1. Most quoted person
2. Person to quote most quotes <- Never actually wrote this one
3. All quotes, in "speaker", "quote" csv format
4. Names that don't match the approved list
5. Quotes that didn't match format, for review of missed names
'''
quote_re = re.compile("^(?:\|\|)?(([a-zA-Z0-9 ()]*):.*)")

messages_that_are_not_quotes = []

quotes_reported = {}

name_translations = {
  "jez": "jerry",
  "ducky": "duck",
  "adom": "adam d",
  "adam": "adam (unspecified)",
  "rae": "raye",
  "dj dizzy drizzle": "shelley",
  "nums (to shelley)": "nums",
  "my dad": "dad",
  "mel to me": "mel",
  "chris (to me)": "chris",
  "mel to adam": "mel",
  "dinni": "dini",
  "gavin": "gav",
  "matt to me": "matt",
  "same girl i work with": "girl at work",
  "girl i work with": "girl at work",
  "mel to dini": "mel",
  "also adam c": "adam c",
  "chris to me": "chris",
  "me": "raye",
  "also my dad": "dad",
  "jared": "jarred"
  }


approved_names = [
  "duck",
  "shelley",
  "nums",
  "chris",
  'mel',
  "jerry",
  "matt",
  "adam d",
  "adam c",
  "adam",
  "jack",
  "mak",
  "raye",
  "gav",
  "dini",
  "dad",
  "adam (unspecified)",
  "jarred",
  "youseff",
  "tam",
  "girl at work",
  "jesse",
  "daniel andrews",
  "alex",
  "6 year old eliza"
  ]

wrong_names = {}

quote_count_per_name = {}

def check_and_correct_name(name: str):
  if name.lower() in name_translations:
    return name_translations[name.lower()]
  return name.lower()

def content_to_name_and_quote(content: str):
  match = quote_re.match(content)
  if match is None:
    messages_that_are_not_quotes.append(content)
    return None, None

  name = match.groups()[1]
  message = match.groups()[0]

  if name == "https":
    messages_that_are_not_quotes.append(content)
    return None, None

  if name == "D":
    messages_that_are_not_quotes.append(content)
    return None, None

  return name, message 


if __name__ == "__main__":
  with open("./quotes_without_context.json", "r") as f:
    quotes = json.load(f)
  
  messages = quotes["messages"]
  quote_report = open("quote_report.csv", "w")

  spamwriter = csv.writer(quote_report, delimiter='|', quotechar='"', quoting=csv.QUOTE_MINIMAL)

  for message in messages:
    name, quote = content_to_name_and_quote(message["content"]) # 5. Quotes that didn't match format handled in here

    if name is not None:
      name = check_and_correct_name(name)
      quoter = message["author"]["name"]

      spamwriter.writerow([name, quote]) # full quote report, gonna load this into google sheets

      if name.lower() not in approved_names: # 4. wrong name report
        if name in wrong_names: 
          wrong_names[name] += 1
        else:
          wrong_names[name] = 1

      # 1. most quoted person
      if name not in quote_count_per_name:
        quote_count_per_name[name] = 0
      quote_count_per_name[name] += 1

      if quoter not in quotes_reported:
        quotes_reported[quoter] = 0
      quotes_reported[quoter] +=1
        

  quote_report.close()

  with open("name_report.txt", "w") as f:
    for name, count in sorted(wrong_names.items(), reverse=True, key=lambda quotes: quotes[1]):
      f.write(f"{name}: {wrong_names[name]}\n")

  with open("rejects.txt", "w") as f:
    for message in messages_that_are_not_quotes:
      f.write(f"{message}\n")

  with open("most_quoted.csv", "w") as f:
    for name, quote in sorted(quote_count_per_name.items(), reverse=True, key=lambda quotes: quotes[1]):
      f.write(f"{name}: {quote}\n")
  
  with open("most_reported.csv", "w") as f:
    for name, quote in sorted(quotes_reported.items(), reverse=True, key=lambda quotes: quotes[1]):
      f.write(f"{name}: {quote}\n")


  # Chris Quote

  # Quotes per person

