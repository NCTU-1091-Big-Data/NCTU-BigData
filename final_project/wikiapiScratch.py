import requests
import csv


# categorylist = ["典范", "甲级", "優良", "乙级", "丙级", "初级", "全部小作品"]
categorylist = ["Featured articles", "Good articles", "B-Class articles", "C-Class articles", "Start-Class articles", "Stub-Class articles"]
languagelist = ["zh", "en"]

category = categorylist[3]
language = languagelist[1]


def scratchtitle(text, titlelist, flag, cmcontinue):
  if len(text) != 0:
    payload = {
        "action": "query",
        "format": "json",
        "list": "categorymembers",
        "cmtitle": text,
        "utf8": 1,
        "cmprop": "title",
        "cmlimit": "max"
        }
    if flag:
      payload.update({"cmcontinue": cmcontinue})
    url = "https://{}.wikipedia.org/w/api.php".format(language)
    resp = requests.get(url, params=payload)
    title = resp.json()
    if "continue" in title:
      cmcontinue = title["continue"]["cmcontinue"]
      scratchtitle(text, titlelist, True, cmcontinue)
    title = title['query']['categorymembers']
    for i in title:
      if i['ns'] == 14:
        scratchtitle(i['title'], titlelist, False, cmcontinue)
      elif i['ns'] == 1:
        # print(len(titlelist))
        titlelist.append(i['title'].replace("Talk:", ""))
      elif i['ns'] == 0:
        # print(len(titlelist))
        titlelist.append(i['title'])

def writetitlecsv(titlelist):
    string = '/content/drive/Shareddrives/NCTU-1091-Big Data/Term Project/維基已分類過條目/{}.csv'.format(category)

    with open(string, 'w', newline='', encoding="utf-8") as csvfile:
      writer = csv.writer(csvfile)
      writer.writerow(['title'])
      for i in range(len(titlelist)):
        writer.writerow([titlelist[i]])

def writecsv():
    # string = '/content/drive/Shareddrives/NCTU-1091-Big Data/Term Project/維基已分類過條目/{}條目.csv'.format(category)
    string = '/content/drive/Shareddrives/NCTU-1091-Big Data/Term Project/維基已分類過條目/{}.csv'.format(category)

    titleNumber = 50
    with open(string, 'w', newline='', encoding="utf-8") as csvfile:
      writer = csv.writer(csvfile)
      writer.writerow(['title', 'context'])
      for i in range(0, len(titlelist), titleNumber):
        string = ""
        if (i + titleNumber) > len(titlelist):
          titleNumber = len(titlelist) - i
        for j in range(titleNumber):
          string = string + titlelist[i + j] + "|"
        string = string[:-1]
        payload = {
          "action": "query",
          "format": "json",
          "prop": "revisions",
          "titles": string,
          "utf8": 1,
          "rvprop": "content"
        }
        url = "https://zh.wikipedia.org/w/api.php"
        resp = requests.get(url, params=payload)
        # print(resp.text)
        string = list(resp.json()['query']['pages'].values())
        for j in range(titleNumber):
          text = string[j]['revisions'][0]['*']
          title = string[j]['title']
          writer.writerow([title, text])

def main():
    titlelist = []
    # string = "Category:{}条目".format(category)  # "典范", "甲级", "乙级", "丙级", "初级"
    # string = "Category:{}條目".format(category)  # "優良" 
    string = "Category:{}".format(category)  # "小作品"   
    scratchtitle(string, titlelist, False, "")
    print(type(titlelist), len(titlelist))
    titlelist = list(set(titlelist))
    print(type(titlelist), len(titlelist))
    writetitlecsv(titlelist)

		

if __name__ == '__main__':
	main()